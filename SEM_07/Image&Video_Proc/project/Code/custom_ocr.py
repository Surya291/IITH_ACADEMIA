from imports import *

'''
This utility takes in an image : in np array and 
--> psm : 04
--> returns data as dataframe to analyse
--> groups all the words wrt block , para, line no
--> removes lines with -1 conf
--> sets a threshold and removes all other lines

---> Creates appropriate spacing betweeen paragraphs and blocks
---> When last sentence does not end with a full stop does not create a new para 
---> Creates and returns a whole multi line string

'''

def OCR(img):
    thresh_0 = 40 ### per word thresh
    thresh = 40
    config = options = "-l {}  --tessdata-dir {} --psm {} --oem {}  ".format('kan+eng',  "/home/surya/Desktop/Lending_Kat/tessdata-best", 6,1)
    
    text_data = pytesseract.image_to_data(Image.fromarray(img), output_type='data.frame', config = config)
    text_data = text_data[text_data.conf > thresh_0]### removing elements with low conf
    #display(text_data)
    
    group_obj = text_data.groupby(['block_num', 'par_num','line_num'], as_index = True)
    
    ### creating a dataframe and removing lines
    df= group_obj['conf'].mean().reset_index()
    #df['line'] = group_obj['text'].apply(lambda x: ' '.join(list(x)) if x=='asdf').tolist()

    df['line'] = group_obj['text'].apply(lambda x: ' '.join(list(x)) ).tolist()
    df = df[df.conf > thresh]
    

    list_lines = []
    prev_line = ''

    bn ,pn,ln = 0,0,0
    for index, row in df.iterrows():
        curr_line = row['line']

        if(row['block_num'] != bn or row['par_num']!= pn):
            bn ,pn= row['block_num'],row['par_num']
            if( len(prev_line)>0 and prev_line[-1] == '.' ):  ### If last line ends with fullstop then start a new para
                list_lines.append('')
        list_lines.append(row['line'])
        prev_line = curr_line
    page_ocr = '\n'.join(list_lines)
    return page_ocr
    
if __name__ == "__main__":
    img_path =  '/home/surya/Desktop/Lending_Kat/Property_docs_for_MVP/kan_expt/expt1/jpg_files/1_SaleDeed-2020/7_cropped.jpg'
    img = cv2.imread(img_path)
    print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = OCR(gray)
    print(text)