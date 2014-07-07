import xml.etree.ElementTree as etree
#ll={"1":[(1,2),(2,1)]} 
def main():
    level={}
    tmp=[]
    tmp2=[]
    tree = etree.parse('levels.xml')
    root = tree.getroot()
    for child in tree.iter():
		
		for c in child:
    			if c.tag != "level":
				if c.tag == "id":
					tmp=[]
					tmp2=[]
					i=c.text
				else:
					
					tmp.append(c.text)
					if len(tmp)==2:
						tupla=tmp[0],tmp[1]
						tmp2.append(tupla)
						tmp=[]
				level[i]=tmp2
						
    return  level
if __name__ == "__main__":
	level=main() 
	print level
