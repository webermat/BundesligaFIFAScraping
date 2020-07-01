import scrapy
import itertools

class BundesligaResults(scrapy.Spider):
    name = 'bundesligaresults'
    allowed_domains = ['www.kicker.de/1-bundesliga/spieltag/1963-64/-1']
    start_urls = ['https://www.kicker.de/1-bundesliga/spieltag/1963-64/-1']

    def parse(self, response):
        spieltag=response.css(".kick__section-headline::text").extract()
        #spieltag appears only once, but we need it for every match
        spieltag_new=list(itertools.chain.from_iterable(itertools.repeat(x, 8) for x in spieltag))
        print("spieltag_new",spieltag_new,len(spieltag_new))
        teams=response.css(".kick__v100-gameCell__team__name::text").extract()
        team_home=teams[0::2]
        team_away=teams[1::2]
        scores=response.css(".kick__v100-scoreBoard__scoreHolder__score::text").extract()
        scores_home=scores[0::4]
        scores_away=scores[1::4]
        scores_home_HT=scores[2::4]
        scores_away_HT=scores[3::4]
        print("away",team_away)
        print("home",team_home)
        #print(teams)
        #test=list(zip(spieltag,teams))
        #print("length test",len(test))
        
        for item in zip(spieltag_new,team_home,team_away,scores_home,scores_away,scores_home_HT,scores_away_HT):
            #create a dictionary to store the scraped info
            print(item)
            scraped_info = {
                'spieltag' : item[0],
                'team_H' : item[1],
                'team_A' : item[2],
                'goal_H' : item[3],
                'goal_A' : item[4],
                'goal_H_HT' : item[5],
                'goal_A_HT' : item[6], 
           }


            #yield or give the scraped info to scrapy
            yield scraped_info
