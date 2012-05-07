#!/bin/sh

FILE=$1

echo "################################################################################"
git log "$FILE"

echo "################################################################################"
echo "which commit"
read commit
echo "################################################################################"

git diff $commit --patch --no-color "$FILE" > /tmp/gitdiffjson

python -c """
file = open('/tmp/gitdiffjson')
lines = file.readlines()

before = []
after = []
for line in lines:
    if line.startswith('---') or line.startswith('+++'):
        continue
    elif line.startswith('-'):
        before.append(line.replace('-', ''))
    elif line.startswith('+'):
        after.append(line.replace('+', ''))

import simplejson as json

before = json.loads('\n'.join(before))
after = json.loads('\n'.join(after))

h_before = dict(map(lambda e: (e['pk'], e), before))
h_after = dict(map(lambda e: (e['pk'], e), after))

for id, element in h_before.items():
    if not id in h_after:
         print '- %s' % element
         continue
    for k,v in element['fields'].items():
         v2 = h_after[id]['fields'].get(k)
         if v != v2:
             print ' pk:%s/%s %s != %s' % (id, k, v, v2)

for id, element in h_after.items():
    if not id in h_before:
         print '+ %s' % element
         continue
    for k,v in element['fields'].items():
         v2 = h_before[id]['fields'].get(k)
         if v != v2:
             print ' pk:%s/%s %s != %s' % (id, k, v, v2)
"""


