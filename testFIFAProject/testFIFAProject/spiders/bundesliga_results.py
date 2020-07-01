import scrapy
import itertools

#start with 3 point Bundesliga aka season 95-96
#34 match day, each day with 18 teams we have 9 matches
class BundesligaResults(scrapy.Spider):
    name = 'bundesligaresults'
    allowed_domains = []#'www.kicker.de/1-bundesliga/spieltag/1963-64/-1','www.kicker.de/1-bundesliga/spieltag/1964-65/-1']
    start_urls=[]
    default_domain='www.kicker.de/1-bundesliga/spieltag/'
    for i in range (1995,2020):
        year_str=str(i+1)
        domain=default_domain+str(i)+"-"+str(i+1)[2:]+"/-1"
        print("domain calculated",domain)
        allowed_domains.append(domain)
        start_urls.append('https://'+domain)
    def parse(self, response):
        url=response.url
        year=int(url[-10:-6])+1
        #print("year",year)
        year_list=[year]*34*9
        spieltag=response.css(".kick__section-headline::text").extract()
        #spieltag appears only once, but we need it for every match, 9 matches
        for i in range(len(spieltag)):
            old_string=spieltag[i]
            #print("old tag", old_string)
            new_string=old_string.replace(" ","")
            new_string=new_string.replace("\r\n","")
            spieltag[i]=new_string
        spieltag_new=list(itertools.chain.from_iterable(itertools.repeat(x, 9) for x in spieltag))
        teams=response.css(".kick__v100-gameCell__team__name::text").extract()
        team_home=teams[0::2]
        team_away=teams[1::2]
        scores=response.css(".kick__v100-scoreBoard__scoreHolder__score::text").extract()
        scores_home=scores[0::4]
        scores_away=scores[1::4]
        scores_home_HT=scores[2::4]
        scores_away_HT=scores[3::4]
        url_test=url.replace("spieltag","tabelle")
        print("url_test",url_test)
        #print("away",team_away)
        #print("home",team_home)
        #print(teams)
        #test=list(zip(spieltag,teams))
        #print("length test",len(test))


        
        for item in zip(year_list,spieltag_new,team_home,team_away,scores_home,scores_away,scores_home_HT,scores_away_HT):
            #create a dictionary to store the scraped info
            print(item)
            spieltag_number=item[1].split('.')[0]
            print("spieltag_nummer",spieltag_number)
            url_next=url_test.replace("-1",spieltag_number)
            print("url_next",url_next)
            scraped_info = {
                'championship_year' : item[0],
                'spieltag' : item[1],
                'team_H' : item[2],
                'team_A' : item[3],
                'goal_H' : item[4],
                'goal_A' : item[5],
                'goal_H_HT' : item[6],
                'goal_A_HT' : item[7], 
           }


            #yield or give the scraped info to scrapy
            yield scraped_info
