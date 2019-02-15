import csv
import re


with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_from_csv = list(rows)

tel_pattern = r'(\+\s*7|8)*(\s*)\(*(\d{3})\)*\-*(\s*)(\d{3})(-*)(\d{2})(-*)(\d{2})(\s*)\(*((доб\.)(\s*)(\d{4}))*\)*'
tel_sub = r'+7(\3)\5-\7-\9\12\14'

contacts = contacts_from_csv[1:]

for contact in contacts:
    contact[5] = re.sub(tel_pattern, tel_sub, contact[5])

fio_pat = r'^([а-яА-ЯёЁ]+)(\s*)(,*)([а-яА-ЯёЁ]+)(\s*)(,?)([а-яА-ЯёЁ]+)*'
fio_sub = r'\1,\4,\7'

res_contacts = []
for contact in contacts:
    tmp_contact = ','.join(contact)
    tmp_contact = re.sub(fio_pat, fio_sub, tmp_contact)
    res_contacts.append(tmp_contact.split(','))

pat_to_compare = r'[а-яА-ЯёЁ]+'
indexes_to_remove = []
arr_to_change = []
for i in range(len(res_contacts)):
    for j in range(i + 1, len(res_contacts)):
        if re.match(pat_to_compare, res_contacts[i][0]).group(0) == \
                re.match(pat_to_compare, res_contacts[j][0]).group(0):
            indexes_to_remove.append(i), indexes_to_remove.append(j)
            con_to_remove = []
            for ind in range(len(res_contacts)):
                if res_contacts[i][ind] == '':
                    con_to_remove.append(res_contacts[i][ind] + res_contacts[j][ind])
                else:
                    con_to_remove.append(res_contacts[i][ind])
            arr_to_change.append(con_to_remove)

for index in reversed(indexes_to_remove):
    del res_contacts[index]
res_contacts += arr_to_change
res_contacts.insert(0, contacts_from_csv[0])

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(res_contacts)
