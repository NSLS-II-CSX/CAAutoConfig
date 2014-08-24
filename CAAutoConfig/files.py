import xml.etree.ElementTree as ET
from xml.dom import minidom
#
# Autoconfig class for archive XML files.
#

class CAFile:
  def __init__(self, filename = None):
    if filename is not None:
      self.openFile(filename);
  def openFile(self, filename):
    """Open archiver XML file"""
    self._tree = ET.parse(filename)
    self._root = self._tree.getroot()
    self._groups = self._root.findall('group')

  def findGroup(self, name):
    """Return an XML element for group name"""
    for g in self._groups:
      if g.find('name').text.strip() == name:
        return CAGroup(g)
    
    # If we are here the group does not exist

    g = ET.SubElement(self._root, 'group')
    n = ET.SubElement(g, 'name')
    n.text = name.strip()
    return CAGroup(g)

  def writeFile(self, filename):
    """Write formatted XML to disk"""
    s = ET.tostring(self._root)

    #Remove all formatting
    s = s.replace('\n','')
    s = s.replace('\t','')
    s = s.replace('\r','')

    f = open(filename, 'w')
    f.write(minidom.parseString(s).toprettyxml())
    f.close()

class CAGroup:
  def __init__(self, group):
    self._group = group
  
    # Cache list of PVs in to a list
    self._pvlist = [c.find('name').text.strip()
                    for c in self._group.findall('channel')]

  def listPVs(self):
    """List all PVs in group"""
    for pv in self._pvlist:
      print pv

  def findPV(self, pv):
    """Check if a PV by name is in the group"""
    return pv.strip() in self._pvlist    

  def addPV(self, pv, period = 1, monitor = True):
    if not pv.strip() in self._pvlist: 

      channelElement = ET.SubElement(self._group, 'channel')

      nameElement = ET.SubElement(channelElement, 'name')
      nameElement.text = pv.strip()

      periodElement  = ET.SubElement(channelElement, 'period')
      periodElement.text = str(period)

      if monitor:
        ET.SubElement(channelElement, 'monitor')

      print "++++ Added PV ", pv

      return True

    else:

      #print "**** Skipped PV ", pv
      return False

if __name__ == "__main__":
  # Run some tests.
  caf = CAFile('engine.xml')
  g = caf.findGroup('misc')
  g.listPVs()
  g.addPV('test.VAL')
  g.addPV('test:prng')
  caf.writeFile('text.xml')
