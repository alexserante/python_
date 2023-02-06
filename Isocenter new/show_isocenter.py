import pydicom
import glob
import os

def organize_isocenter(array): #organiza os valor do iso para formato da RT
    x = round(array[0] / 10, 2)
    y = round(array[2] / 10, 2)
    z = -1*round(array[1] / 10, 2)
    iso = [x, y, z]
    return iso

def organize_date(string): #organiza a data no formato DD/MM/YYYY
    year = string[0] + string[1] + string[2] + string[3]
    month = string[4] + string[5]
    day = string[6] + string[7]
    date = day +'/'+ month +'/'+ year
    return date

print("##############################################################################")
print("#                                                                            #")
print("#                         XVI CBCT isocenter check                           #")
print("#                                                                            #")
print("##############################################################################")
print("Version: 08/2021                                          not for clinical use", "\n")



while 'TRUE':
    #cria o caminho para o paciente específico a partir do PACS digitado
    PACS = input("Digite o PACS: ")
    path_to_file = "D:/db/patient_{0}/DICOM_PLAN/*.DCM".format(PACS)

    check_dir = "D:/db/patient_{0}".format(PACS) #checa se o diretório
    isDir = os.path.isdir(check_dir)             #com o PACS específicado existe

    print()

    if isDir:
        for filename in glob.glob(path_to_file): #abre cada um dos arquivos no diretório específicado
            try:
                ds = pydicom.filereader.read_file(filename)
            except:
                print("Não foi possível abrir o arquivo")

            print('Name:', ds[0x0010, 0x0010].value)
            print('PACS:', ds[0x0010,0x0020].value)
            print('Birth date:', organize_date(ds[0x0010, 0x0030].value))
            print('CT date:', organize_date(ds[0x0008, 0x0020].value))
            print('Plan name:', ds[0x300a, 0x0003].value)
            print('Plan date:', organize_date(ds[0x0300a, 0x0006].value))
            print('Plan status:', ds[0x300e, 0x0002].value)
            print('Plan approval date:', organize_date(ds[0x300e, 0x0004].value))

            n_beams = ds[0x300a, 0x0070][0][0x300a, 0x0080].value
            n = 0
            while n < n_beams:
                isocenter_raw = ds[0x300a, 0x00b0][n][0x300a, 0x0111][0][0x300a, 0x012c].value
                isocenter = organize_isocenter(isocenter_raw)

                print('Beam :', ds[0x300a, 0x00b0][n][0x300a, 0x00c3].value , ds[0x300a, 0x00b0][n][0x300a, 0x00ce].value , isocenter)
                n = n + 1


            print('\n', '----------------------------------------------------------------', '\n')

    else:
        print('PACS não existe!')
