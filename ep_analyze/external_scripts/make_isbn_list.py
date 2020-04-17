import sys, os, csv
from pdf_reader.get_isbn import get_isbn



with open('filelist.csv', 'r') as csvfile:
    csv_r = csv.reader(csvfile, delimiter='\t')
    with open('isbnlist.csv', 'w', newline='') as outcsv:
        csv_w = csv.writer(outcsv, delimiter='\t')

        count = 0
        for row in csv_r:
            count += 1
            # if count > 10: break
            pdf_path = row[2]
            if not os.path.isfile(pdf_path): continue
            try: 
                isbn_like, found_at_page = get_isbn(pdf_path, 8)
                if not isbn_like == 'isbn_not_found':
                    row = (pdf_path, isbn_like, found_at_page)
                    csv_w.writerow(row)
                    print(count, pdf_path, isbn_like, found_at_page)
            except Exception as e:
                sys.stderr.write(pdf_path+'\t'+str(e)+'\n')


        
