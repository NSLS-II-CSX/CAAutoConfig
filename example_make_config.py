from CAAutoConfig import utils, files

def main():
  # Get list
  list = utils.getCfPVlist('/cf-update','xf23id?-ioc1.va-01.dbl')
  list = utils.applyRegexToList(list, ['^XF:23ID(A|1|2)*-VA', '.*(?<!_)$'])

  caf = files.CAFile('engine.xml')
 
  group_a = caf.findGroup('23IDA')
  list_a = utils.applyRegexToList(list, ['^XF:23IDA', '^((?!RGA).)*$'])
  for pv in list_a:
    group_a.addPV(pv)

  group_1 = caf.findGroup('23ID1')
  list_1 = utils.applyRegexToList(list, ['^XF:23ID1','^((?!RGA).)*$'])
  for pv in list_1:
    group_1.addPV(pv)

  group_2 = caf.findGroup('23ID2')
  list_2 = utils.applyRegexToList(list, ['^XF:23ID2','^((?!RGA).)*$'])
  for pv in list_2:
    group_2.addPV(pv)

  #group_3 = caf.findGroup('23ID')
  #list_3 = utils.applyRegexToList(list, '^XF:23ID')
  #for pv in list_3:
  #  group_3.addPV(pv)

  caf.writeFile('engine.xml')   
if __name__ == "__main__":
  main()
