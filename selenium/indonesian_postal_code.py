import time
import json
import pandas as pd
from selenium import webdriver

#Input URL
# url = input('Input Indonesian Postal Code Data Website URL :')
# Postal Code
# url = "https://www.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=200&urut=&asc=000101&sby=010000&no1=21401&no2=21600&kk=109"
url = "https://www.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=&jobs=&perhal=200&urut=&asc=000101&sby=010000&no1=82801&no2=83000&kk=416"
# Province
# url = "https://www.nomor.net/_kodepos.php?_i=provinsi-kodepos&sby=010000"
# City
# url = "https://www.nomor.net/_kodepos.php?_i=kota-kodepos&sby=010000"
# District
# url = "https://www.nomor.net/_kodepos.php?_i=kecamatan-kodepos&sby=010000"
# url = "https://www.nomor.net/_kodepos.php?_i=kecamatan-kodepos&daerah=&jobs=&perhal=200&urut=&asc=001000&sby=010000&no1=7001&no2=7200&kk=36"
print(url)
print("Getting URL...")
time.sleep(1)

# Selenium configuration
PATH = "E:\Matin\System Computer\Service\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(url)


current_page = 416
loop = True

table_heads = []
table_body = []
try:
    while loop:
        print("current")
        print(current_page)

        # Get Table
        tables = driver.find_elements_by_xpath("//table[@bgcolor='#ffccff']")
        for table in tables:
            postal_code_tables_headers = table.find_elements_by_xpath("//tr[@bgcolor='darkblue']")
            if not postal_code_tables_headers:
                postal_code_tables_headers = table.find_elements_by_xpath("//tr[@bgcolor='darkgreen']")
                if not postal_code_tables_headers:
                    postal_code_tables_headers = table.find_elements_by_xpath("//tr[@bgcolor='#663300']")
                if not postal_code_tables_headers:
                    postal_code_tables_headers = table.find_elements_by_xpath("//tr[@bgcolor='#330033']")

            # print(postal_code_tables_headers)
            postal_code_tables_bodies = table.find_elements_by_xpath("//tr[@bgcolor='#ccffff']")
            if not postal_code_tables_bodies:
                postal_code_tables_bodies = table.find_elements_by_class_name("cstr")

            if current_page == 416:
                if postal_code_tables_headers:
                    for postal_code_table in postal_code_tables_headers:
                        table_headers = postal_code_table.find_elements_by_tag_name("td")
                        for table_head in table_headers:
                            header = table_head.text.strip()
                            header = header.replace("\n", " ")
                            if header != '' and header not in table_heads and header != "DT2" and header != "Kota, Kabupaten":
                                if header != "DT2 Kota, Kabupaten":
                                    table_heads.append(header)
                                else:
                                    if "DT2" not in table_heads and "Kota, Kabupaten" not in table_heads:
                                        table_heads.append("DT2")
                                        table_heads.append("Kota, Kabupaten")

            print(postal_code_tables_bodies)
            if postal_code_tables_bodies:
                for postal_code_tables_body in postal_code_tables_bodies:
                    body_elements = postal_code_tables_body.find_elements_by_tag_name("td")
                    dict = {}
                    for index, body in enumerate(body_elements):
                        body_text = body.text.strip()
                        body_head = table_heads[index]
                        print(body_head)
                        print(body_text)
                        dict[body_head] = body_text
                        if index == len(table_heads) - 1:
                            print(dict)
                            if dict not in table_body:
                                table_body.append(dict)



        # Get Pagging object
        pagging = driver.find_elements_by_class_name("tpage")
        if len(pagging) > 0:
            # Get Last Page
            last_page = [x.text for x in pagging]
            last_page = int(last_page[-1]) if last_page[-1].isdigit() else int(last_page[-2])
            print("last_page")
            print(last_page)
            for page in pagging:
                print(page.text)
                if int(page.text) > current_page:
                    print("clicked")
                    current_page += 1
                    page.click()
                    break

            if current_page > int(last_page):
                print("end of page")
                print(current_page)
                loop = False
        else:
            loop = False

    if len(table_body) > 0:
        # Create DataFrame
        df = pd.DataFrame(table_body)
        print(df)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('postal_code3.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Province', index=False)
        writer.save()

    print(len(table_body))
    driver.close()
except Exception as e:
    print(e)
    if len(table_body) > 0:
        # Create DataFrame
        df = pd.DataFrame(table_body)
        print(df)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('postal_code3.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Province', index=False)
        writer.save()