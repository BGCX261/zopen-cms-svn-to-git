# -*- encoding:utf-8 -*-

from repoze.bfg.chameleon_zpt import render_template

from z3c.batching.batch import Batch

from interfaces import IHTMLRenderer
from utils import getDisplayTime

def batch_view(context, request):
    kss_next_number = 0
    next_url = ''
    previous_url = ''
    kss_previous_number = 0
   
    batch_start = int(request.params.get('b_start', 0))  

    posts = context.get_recent_file_subpaths()

    batch = Batch(posts, start=batch_start, size=5)
    batch_size = batch.size
    batch_total = batch.total
    if batch.previous:
        previous_url = item_url(context, request, batch.previous.start)
        kss_previous_number = batch.previous.start
    if batch.next:
        next_url = item_url(context, request, batch.next.start)
        if batch.next.start:
            kss_next_number = batch.next.start
    batch_number = batch.number

    count = 0
    previous_batchs = []
    mybatch = batch
    while mybatch.previous:
        count = count + 1
        if count > 2:
            break
        previous_batchs.append(mybatch.previous)
        mybatch = mybatch.previous
    previous_batchs.reverse()
        
    count = 0
    next_batchs = []
    mybatch = batch
    while mybatch.next:
        count = count + 1
        if count > 2:
            break
        next_batchs.append(mybatch.next)
        mybatch = mybatch.next
    
    last_batch = None
    if batch.total-2 > batch.number:
        last_batch = batch.batches[batch.total-1]

    first_batch = None
    if batch.number-2 > 1:
        first_batch = batch.batches[0]

    return render_template('templates/batch.pt',
                            batch = batch,
                            batch_total = batch_total,
                            previous_url = previous_url,
                            kss_previous_number = kss_previous_number,
                            batch_size = batch_size,
                            kss_next_number = kss_next_number,
                            next_url = next_url,
                            first_batch = first_batch,
                            previous_batchs = previous_batchs,
                            next_batchs = next_batchs,
                            last_batch = last_batch,
                            )

def item_url(context, request, b_start):
    item_url = ''
    page_url = str(request.url).split('?')[0]
    if len(request.params) == 0:
        item_url = page_url + '?b_start=' + str(b_start)
    elif len(request.params) == 1 and request.params.has_key('b_start'):
        item_url = page_url + '?b_start=' + str(b_start)
    else:
        if request.params.has_key('b_start'):
            del request.params[0]
        key = request.params.keys()[0]
        item_url = page_url + '?%s=%s' % (key, request.params.get(key))
        for key in request.params.keys()[1:]:
            item_url = item_url + '&%s=%s' % (key, request.params.get(key))
        item_url = item_url + '&b_start=' + str(b_start)
    return item_url


