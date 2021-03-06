import json
from multiprocessing import Pool

import requests

__author__ = 'ApigeeCorporation'

nodes_c32xl = [
    'res000eu',
    'res001eu',
    'res002eu',
    'res003eu',
    'res004eu',
    'res005eu',
    'res009eu',
    'res010eu',
    'res011eu',
    'res012eu',
    'res013eu',
    'res014eu',
]

nodes_c34xl = [
    'res015eu',
    'res018eu',
    'res019eu',
    'res020eu',
    'res021eu',
    'res022eu',
    'res023eu',
    'res024eu',
    'res025eu',
    'res026eu',
    'res027eu',
    'res028eu'
]

nodes = nodes_c34xl

url_base = 'http://localhost:9200'

nodes_string = ",".join(nodes)

payload = {
    "index.routing.allocation.include._host": "",
    "index.routing.allocation.exclude._host": nodes_string
}

# payload = {
#     "index.routing.allocation.include._host": "",
#     "index.routing.allocation.exclude._host": ""
# }

print json.dumps(payload )


r = requests.get(url_base + "/_stats")
indices = r.json()['indices']

print 'retrieved %s indices' % len(indices)

includes = [
    # '70be096e-c2e1-11e4-8a55-12b4f5e28868',
    # 'b0c640af-bc6c-11e4-b078-12b4f5e28868',
    # 'e62e465e-bccc-11e4-b078-12b4f5e28868',
    # 'd82b6413-bccc-11e4-b078-12b4f5e28868',
    # '45914256-c27f-11e4-8a55-12b4f5e28868',
    # '2776a776-c27f-11e4-8a55-12b4f5e28868',
    # 'a54f878c-bc6c-11e4-b044-0e4cd56e19cd',
    # 'ed5b47ea-bccc-11e4-b078-12b4f5e28868',
    # 'bd4874ab-bccc-11e4-b044-0e4cd56e19cd',
    # '3d748996-c27f-11e4-8a55-12b4f5e28868',
    # '1daab807-c27f-11e4-8a55-12b4f5e28868',
    # 'd0c4f0da-d961-11e4-849d-12b4f5e28868',
    # '93e756ac-bc4e-11e4-92ae-12b4f5e28868',
    #
    # 'b6768a08-b5d5-11e3-a495-11ddb1de66c8',
    # 'b6768a08-b5d5-11e3-a495-10ddb1de66c3',
    # 'b6768a08-b5d5-11e3-a495-11ddb1de66c9',
]

excludes = [
    #
    # '70be096e-c2e1-11e4-8a55-12b4f5e28868',
    # 'b0c640af-bc6c-11e4-b078-12b4f5e28868',
    # 'e62e465e-bccc-11e4-b078-12b4f5e28868',
    # 'd82b6413-bccc-11e4-b078-12b4f5e28868',
    # '45914256-c27f-11e4-8a55-12b4f5e28868',
    # '2776a776-c27f-11e4-8a55-12b4f5e28868',
    # 'a54f878c-bc6c-11e4-b044-0e4cd56e19cd',
    # 'ed5b47ea-bccc-11e4-b078-12b4f5e28868',
    # 'bd4874ab-bccc-11e4-b044-0e4cd56e19cd',
    # '3d748996-c27f-11e4-8a55-12b4f5e28868',
    # '1daab807-c27f-11e4-8a55-12b4f5e28868',
    # 'd0c4f0da-d961-11e4-849d-12b4f5e28868',
    # '93e756ac-bc4e-11e4-92ae-12b4f5e28868',
    #
    # 'b6768a08-b5d5-11e3-a495-11ddb1de66c8',
    # 'b6768a08-b5d5-11e3-a495-10ddb1de66c3',
    # 'b6768a08-b5d5-11e3-a495-11ddb1de66c9',
]

counter = 0
update = False

for index_name in indices:
    update = False
    counter += 1

    # print 'Checking index %s of %s: %s' % (counter, len(indices), index_name)

    if len(includes) == 0:
        update = True
    else:
        for include in includes:

            if include in index_name:
                update = True

    if len(excludes) > 0:
        for exclude in excludes:
            if exclude in index_name:
                update = False

    if not update:
        print 'Skipping %s of %s: %s' % (counter, len(indices), index_name)
    else:
        print '+++++Processing %s of %s: %s' % (counter, len(indices), index_name)

        url_template = '%s/%s/_settings' % (url_base, index_name)
        print url_template

        success = False

        while not success:

            response = requests.put('%s/%s/_settings' % (url_base, index_name), data=json.dumps(payload))

            if response.status_code == 200:
                success = True
                print '200: %s: %s' % (index_name, response.text)
            else:
                print '%s: %s: %s' % (response.status_code, index_name, response.text)
