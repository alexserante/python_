import pydicom #https://pydicom.github.io/pydicom/stable/tutorials/
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset

path_to_files = 'L:/Radioterapia/Fisicos/ARS/ATOM/Modificar planos DCM/Planos/' #diretorio dos arquivos .dcm
path_to_files_mod = 'L:/Radioterapia/Fisicos/ARS/ATOM/Modificar planos DCM/Planos_mod/'

list_files = ['PROSTATE.dcm']
'''
for k in range(1,9):
  list_files.append(str(k) + '.dcm')
'''
print(list_files)

for dcm_file in list_files: #percorre todos os arquivos da lista
    try:
        ds = pydicom.filereader.read_file(path_to_files + dcm_file) #carrega o arquivo dicom

        #Tentativa de modificar o cabeçalho do DCM para o dicomtree exportar o arquivo para o MOSAIQ
        #utilizando dados de um paciente
        patient_name = ds[0x0010, 0x0010]
        new_patient_name = 'ANTENOR MORAES'
        patient_name.value = new_patient_name

        patient_ID = ds[0x0010, 0x0020]
        new_patient_ID = '12270256'
        patient_ID.value = new_patient_ID

        patient_birth_date = ds[0x0010, 0x0030]
        new_patient_birth_date = '19280517'
        patient_birth_date.value = new_patient_birth_date

        patient_sex = ds[0x0010, 0x0040]
        new_patient_sex = 'M'
        patient_sex.value = new_patient_sex

        other_patient_name = ds[0x0010, 0x1001]
        other_patient_name.value = new_patient_name

        other_patient_ID = ds[0x0010, 0x1000]
        other_patient_ID.value = new_patient_ID

        plan_name = ds[0x300a, 0x0003]
        new_plan_name = plan_name.value + 'Mod'
        plan_name.value = new_plan_name

        plan_name_label = ds[0x300a, 0x0002]
        new_plan_name_label = plan_name_label.value + 'Mod'
        plan_name_label.value = new_plan_name_label

        instance_creator_UID = ds[0x0008, 0x0014]
        aux = '2.16.840.1.114337'
        instance_creator_UID.value = aux

        SOP_instance_UID = ds[0x0008, 0x0018]
        aux = '2.16.840.1.114337.1.1.1635443768.0'
        SOP_instance_UID.value = aux

        study_instance_UID = ds[0x0020, 0x000d]
        aux = '1.2.840.113704.1.111.7148.1621279643.1'
        study_instance_UID.value = aux

        series_instance_UID = ds[0x0020, 0x000e]
        aux = '2.16.840.1.114337.1635443768'
        series_instance_UID.value = aux


        status = ds[0x300e, 0x0002]
        status.value = 'UNAPPROVED'
        try:
            del ds[0x300e, 0x0004]
            del ds[0x300e, 0x0005]
            del ds[0x300e, 0x0008]
        except:
            print('Status ok')

#inicio da modificacao das laminas do MLC
        # desloca em 'inc' a posicao da laminas de apenas um banco
        inc = 1

        for beam in ds[0x300a, 0x00b0]: #percorre todos os campos/arcos do plano
            if beam[0x300a, 0x00ce].value == 'TREATMENT': #verifica se é campo de tratamento
                for cp in beam[0x300a, 0x0111]: #percorre todos os control points
                    leaf_pos = cp[0x300a, 0x011a][2][0x300a, 0x011c]
                    leaf_pos_temp = []
                    cont = 1
                    print(cp[0x300a, 0x011a][2][0x300a, 0x011c].value)
                    for leaf in leaf_pos: #percorre todas as laminas nesse cp
                        if cont>40: # modifica laminas de x2
                            leaf = leaf + inc
                        else: # modifica laminas de x1
                            leaf = leaf - inc #mm

                        leaf = round(leaf, 1)

                        cont += 1
                        leaf_pos_temp.append(leaf)
                    leaf_pos.value = leaf_pos_temp #atribui os valores alterados ao dataset
                    print(cp[0x300a, 0x011a][2][0x300a, 0x011c].value)

        ds.save_as(path_to_files_mod + 'Modificado_' + dcm_file)

    except:
        print('Não foi possível alterar o arquivo ' + dcm_file)
