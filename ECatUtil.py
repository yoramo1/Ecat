import sys
import os
import YoUtil
import ECatConfigUtil
from ECatEsiUtil import EsiUtil as EsiUtil
from ECatEsiUtil import EsiFile as EsiFile
from YoUtil import ecat_excel_util as excel
from YoUtil import print_util as pr
import click

#---------------------------------
#click site: https://github.com/pallets/click
#            https://click.palletsprojects.com/en/latest/
#tutorial -  https://dbader.org/blog/mastering-click-advanced-python-command-line-apps
#---------------------------------


@click.group()
def cli():
	pass

@click.command()
@click.option('--excel',help='generate a excel file',type=click.Path())
@click.option('--elmo',help='load elmo special', default=False,is_flag=True)
@click.argument('cfg_file',  type=click.Path())
def config(cfg_file,excel,elmo=False):
	'''  
	Dispay a full config
	[--excel] - generate a Excel file 
	'''
	if os.path.isfile(cfg_file):
		pr1 = pr()
		cfg = ECatConfigUtil.Config(cfg_file)
		cfg.load_config()
		master = cfg.get_master();
		slave_list = cfg.get_slaves()
		if elmo!= None:
			elmoSpecial = cfg.get_elmospecial()
		else:
			elmoSpecial = None
		str = ''
		if master!=None:
			str += master.tostring(1)
		for s in slave_list:
			str += s.tostring(1)
		if elmoSpecial!= None:
			str += elmoSpecial.tostring(1)
		pr1.print(str)
		if excel != None:
			generate_excel(cfg, excel)
	else:
		pr.print ('Error: [%s] is not a file '% cfg_file)

@click.command()
@click.argument('cfg_file',  type=click.Path())
def slave_names(cfg_file):
	'''
	list slave names
	'''
	if os.path.isfile(cfg_file):
		pr1 = pr()
		cfg = ECatConfigUtil.Config(cfg_file)
		cfg.load_config()
		slave_list = cfg.get_slaves_names()
		pr1.print(slave_list)
	pass

def generate_excel(cfg,excel_file):
	slave_list = cfg.get_slaves()
	xlsx = excel()
	xlsx.create_file(excel_file)
	num=0
	for s in slave_list:
		name = s.name_in_res
		if name is None:
			name = 'Slave '+str(num)
		xlsx.append_slave_initCmd(s,name)
		num+=1
	xlsx.close()

@click.command()
@click.option('-vendor',  type=str, default=None)
@click.option('-product',  type=str, default=None)
def find_esi(vendor,product):
	'''
		finds ESI files can fileter by [vendor] and [product]
	'''
	pr1= pr()
	esi = EsiUtil()
	vendor_id = None
	productCode=None
	if vendor!=None:
		vendor_id = YoUtil.get_int(vendor)
	if product!= None:
		productCode = YoUtil.get_int(product)
	files = esi.get_ESI_files(vendor_id,productCode)
	if files != None and len(files)>0:
		YoUtil.print_list(files,1)
	else:
		pr1.print('ESI not found !')
	
@click.command()
@click.argument('esi_path',  type=click.Path())
def esi_devices(esi_path):
	'''
	dispay the devices in a ESI file
	'''
	pr1= pr()
	esi_file = EsiFile(esi_path)
	if esi_file != None:
		esi_file.load_devices()
		for d in esi_file.devices:
			pr1.print('(0x%x,0x%x) - %s' % (d.product_code, d.revision, d.name))
		pass
	else:
		pr1.print('Error loading ESI file')
	pass
	
@click.command()
def esi_folders():
	'''
	gets the list of folders that holds ESI files
	'''
	pr1= pr()
	esi = EsiUtil()
	folders = esi.get_ESI_folders()
	YoUtil.print_list(folders,1)
	
	
@click.command()
@click.argument('ws_path',  type=click.Path())
def workspace(ws_path):
	pass

#Add Commands
cli.add_command(config)
cli.add_command(slave_names)
cli.add_command(find_esi)
cli.add_command(esi_devices)
cli.add_command(esi_folders)
cli.add_command(workspace)

		
if (__name__=='__main__'):
	cli()
	