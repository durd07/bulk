#!/usr/bin/env python
# -*- codeing: utf-8 -*-

class Tag():
    def __init__(self):
        pass

tagList1 = []
tagList2 = []

from xml.dom.minidom import parse, parseString
doc = parse('tag_config.xml')
for node in doc.getElementsByTagName('Berth'):
    ID = node.getAttribute('ID')
    num = node.getElementsByTagName('num')[0].firstChild.nodeValue
    name = node.getElementsByTagName('name')[0].firstChild.nodeValue
    tag = Tag()
    tag.ID = ID
    tag.num = num
    tag.name = name
    tagList1.append(tag)

doc = parse('tag_config2.xml')
for node in doc.getElementsByTagName('Berth'):
    ID = node.getAttribute('ID')
    num = node.getElementsByTagName('num')[0].firstChild.nodeValue
    name = node.getElementsByTagName('name')[0].firstChild.nodeValue
    tag = Tag()
    tag.ID = ID
    tag.num = num
    tag.name = name
    tagList2.append(tag)

for tag in tagList2:
    for tag1 in tagList1:
        if tag.name == tag1.name:
            tag.num = tag1.num

from xml.dom.minidom import Document

doc = Document()

root = doc.createElement('Probe')
doc.appendChild(root)

for tag in tagList2:
    item = doc.createElement('Berth')
    item.setAttribute('ID', tag.ID)
    root.appendChild(item)
    numtag = doc.createElement('num')
    numtext = doc.createTextNode(tag.num)
    numtag.appendChild(numtext)

    nametag = doc.createElement('name')
    nametext = doc.createTextNode(tag.name)
    nametag.appendChild(nametext)
    item.appendChild(numtag)
    item.appendChild(nametag)

f = open('tag_config_new.xml', 'w')
f.write(doc.toprettyxml(indent = '  '))
f.close


