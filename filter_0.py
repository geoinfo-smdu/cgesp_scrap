txt = open("com_falhas.js","r")
content = txt.read() 

new_file = open('novo.js','w')
new_file.write(content)

txt.close()
new_file.close()