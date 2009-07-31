import sys
import settings
import urllib
import json

def get_titles(domain):
    url = '/ysearch/web/v1/site:%s?appid=%s&format=json&count=50' % \
        (domain, settings.BOSS_API_KEY)
    return _extract_titles(url)
    
def _extract_titles(url):
    f = urllib.urlopen(settings.BOSS_HOST+url)
    bossobj = json.load(f)
    f.close()
    titles = []
    for result in bossobj['ysearchresponse']['resultset_web']:
        titles.append(result['title'])
        
    if bossobj['ysearchresponse'].get('nextpage') and bossobj['ysearchresponse'].get('nextpage') != url:
        if settings.DEBUG:
            print bossobj['ysearchresponse']['nextpage']
        titles += _extract_titles(bossobj['ysearchresponse']['nextpage'])
    return titles

def calculate_variety(url):
    titles = get_titles(sys.argv[1])
    num_titles = len(titles)
    print "%d titles found for %s"%(num_titles, url)
    unique_titles = len(set(titles))
    print "%d unique titles found for %s" %(len(set(titles)), url)
    percentage = float(unique_titles)/num_titles * 100
    print "%d%% of the pages on %s have unique titles" % (percentage, url)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s domain.com"%sys.argv[0]
        sys.exit(1)
    
    calculate_variety(sys.argv[1])
