import pandas as pd 
import xlsxwriter
import openpyxl
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw.MolDrawing import MolDrawing,DrawingOptions
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
smiles_filename = 'data_grouped.csv'
save_filename = 'data_grouped_with_images.xlsx'
smiles_filepath = os.path.join(base_dir,smiles_filename)
imgs_savefolder = os.path.join(base_dir,'molecule_images')
save_path = os.path.join(base_dir,save_filename)

if not os.path.exists(imgs_savefolder):
    os.mkdir(imgs_savefolder)
 
# df = pd.read_excel(smiles_filepath, engine='openpyxl',header=0)
df = pd.read_csv(smiles_filepath, header=0, sep="\t")
 
def transparent_draw(smiles):
    mol = Chem.MolFromSmiles(smiles)
    img = Draw.MolToImage(mol, size=(256, 128))
    img = img.convert('L')
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def generation_images(data):
    smileses = data.Smiles.tolist()
    for i,smiles in enumerate(smileses):
        draw = transparent_draw(smiles)
        draw.save(imgs_savefolder+'/img{}.png'.format(i))
        # Draw.MolToFile(mol,os.path.join(imgs_savefolder,'img{}.png'.format(i)),size=(150,100))


def load_images(data):
    # No	smiles	group	closeness centrality
    workbook = xlsxwriter.Workbook(save_path,{'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0,3,10)
    worksheet.set_column("G:G", 20) #cs
    worksheet.set_column("D:D", 100) #Smiles
    worksheet.set_column("H:H", 20.3) #Image
    worksheet.set_default_row(74)
    worksheet.write('A1', 'No')
    worksheet.write('B1', 'ID')
    worksheet.write('C1', 'Name')
    worksheet.write('D1', 'Smiles')
    worksheet.write('E1', 'Group')
    worksheet.write('F1', 'Color')
    worksheet.write('G1', 'ClosenessCentrality')
    worksheet.write('H1', 'Image')
    
    for index, row in data.iterrows():
        worksheet.write(f'A{index+2}', row['No'])
        worksheet.write(f'B{index+2}', row['ID'])
        worksheet.write(f'C{index+2}', row['Name'])
        worksheet.write(f'D{index+2}', row['Smiles'])
        worksheet.write(f'E{index+2}', row['Group'])
        worksheet.write(f'F{index+2}', row['Color'])
        worksheet.write(f'G{index+2}', row['ClosenessCentrality'])
        worksheet.insert_image(f'H{index+2}', os.path.join(imgs_savefolder,'img{}.png'.format(index)))
    workbook.close()
    # for i,j in enumerate(data):
    #     # worksheet.write(f'A{i+1}', f'{j}')
    #     worksheet.insert_image(f'E{i+2}', os.path.join(imgs_savefolder,'img{}.png'.format(i)))
    # workbook.close()
 
generation_images(df)
load_images(df)

