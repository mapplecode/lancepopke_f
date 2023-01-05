import xml.etree.ElementTree as ET

data = ET.Element('chess')
b_xml = ET.tostring(data)
with open("GFG.xml", "wb") as f:
	f.write(b_xml)
