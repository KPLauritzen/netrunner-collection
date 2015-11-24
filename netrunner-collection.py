from __future__ import print_function
import requests
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--deckid', type=str, default='26062',
                    help='ID of netrunnerdb deck to download')
args = parser.parse_args()

root_url = 'http://www.netrunnerdb.com'


def download_card_by_id(id):
    """
    Checks if that card already has been downloaded.
    Otherwise it downloads the card png.
    """
    if os.path.isfile('./imgs/{id}.png'.format(**locals())):
        # We already have the card
        pass
    else:
        req = requests.get(root_url + '/api/card/' + str(id))
        req.raise_for_status()

        img_url = req.json()[0]['imagesrc']

        img_req = requests.get(root_url + img_url)
        img_req.raise_for_status()

        f = open('./imgs/{id}.png'.format(**locals()), 'wb')
        f.write(img_req.content)
        f.close()


def get_cards_in_decklist(id):
    """
    Get card ids and counts from a decklist on netrunnerdb.com
    """
    req = requests.get(root_url + '/api/decklist/' + str(id))
    req.raise_for_status()
    cards = req.json()['cards']
    return cards


def append_collection(f, id, count):
    """
    Add a card 'count' times to the file 'f'.
    """
    for i in range(count):
        f.write('<img src=imgs/{id}.png width=228>\n'.format(**locals()))

if __name__ == '__main__':
    # Make sure the 'imgs/' dir exists
    if not os.path.exists('./imgs/'):
        os.makedirs('./imgs/')

    cards = get_cards_in_decklist(args.deckid)
    f = open('collection.html', 'w')
    for card_id, card_count in cards.iteritems():
        download_card_by_id(card_id)
        append_collection(f, card_id, card_count)

    f.close()
