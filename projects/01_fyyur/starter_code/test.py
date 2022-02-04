import re
from flask import session
from app import db,Venue,Artist,shows, venues
from sqlalchemy import select
from sqlalchemy.orm import Bundle
import forms
from forms import ShowForm
from collections import ChainMap
# from sqlalchemy import func
# data = list()
# states = Venue.query.with_entities(Venue.state).distinct().all()
# i = 0
# for state in states:
#     state = state[0]
#     citites = Venue.query.with_entities(Venue.city).filter(Venue.state==state).distinct().all()
#     for city in citites:
#         city = city[0]
#         subdata = dict()
#         subdata['city'] = city
#         subdata['state'] = state
#         venues = Venue.query.with_entities(Venue.id,Venue.name).filter(Venue.state==state,Venue.city==city).distinct().all()
#         subdata['venues'] = venues
#         data.append(subdata)

# print(data)
# VenueData=dict()
# # VenueData['id']=Venue.query.with_entities(Venue.id).filter(Venue.id == 18).all()
# # VenueData['name']=Venue.query.with_entities(Venue.name).filter(Venue.id == 18).all()
# # VenueData['city']=Venue.query.with_entities(Venue.city).filter(Venue.id == 18).all()
# # VenueData['state']=Venue.query.with_entities(Venue.state).filter(Venue.id == 18).all()
# # VenueData['address']=Venue.query.with_entities(Venue.address).filter(Venue.id == 18).all()
# # VenueData['phone']=Venue.query.with_entities(Venue.phone).filter(Venue.id == 18).all()
# # VenueData['facebook_link']=Venue.query.with_entities(Venue.facebook_link).filter(Venue.id == 18).all()
# # VenueData['website_link']=Venue.query.with_entities(Venue.website_link).filter(Venue.id == 18).all()
# # VenueData['image_link']=Venue.query.with_entities(Venue.image_link).filter(Venue.id == 18).all()
# # VenueData['seeking_description']=Venue.query.with_entities(Venue.seeking_description).filter(Venue.id == 18).all()
# # VenueData['looking_for_talent']=Venue.query.with_entities(Venue.looking_for_talent).filter(Venue.id == 18).all()
# # VenueData['genres']=Venue.query.with_entities(Venue.genres).filter(Venue.id == 18).all()
# # VenueData.items()
# # venueList =[each.looking_for_talent for each in  Venue.query.with_entities(Venue.looking_for_talent).filter(Venue.id == 18)]
# # print(venueList)
# VenueData = dict()
# VenueList= Venue.query.with_entities(Venue.id,Venue.name,Venue.city,Venue.state,Venue.address,Venue.facebook_link,Venue.website_link,Venue.image_link,Venue.seeking_description,Venue.looking_for_talent).filter(Venue.id==18).all()
# genres = Venue.query.with_entities(Venue.genres).filter(Venue.id==18).all()

# genres = genres[0][0].split(',')
# length = len(genres)
# for i in range(length):
#     for char in '{ }':
#         genres[i] = genres[i].replace(char,'')

# for v in VenueList:
#     VenueData['id'] = v[0]
#     VenueData['name'] = v[1]
#     VenueData['city'] = v[2]
#     VenueData['state'] = v[3]
#     VenueData['address'] = v[4]
#     VenueData['facebook_link'] = v[5]
#     VenueData['website_link'] = v[6]
#     VenueData['image_link'] = v[7]
#     VenueData['seeking_description'] = v[8]
#     VenueData['looking_for_talent'] = v[9]

   
#     VenueData['genres'] = genres
    
# print(VenueData)


# data = Venue.query.get(18)

# for d in data:
#     VenueData['id'] = data.id 

#     print(VenueData)


# for ven in VenueData:
#     dic = {}
#     dic['id'] = 






# ArtisitDict = dict()
# ArtistList = Artist.query.with_entities(Artist.id,Artist.name,Artist.city,Artist.state,Artist.phone,Artist.looking_for_venues,
# Artist.image_link,
# Artist.facebook_link,
# Artist.website_link,
# Artist.seeking_description
# ).filter(Artist.id==artist_id).all()
# ArtistGenres = Artist.query.with_entites(Artist.genres).filter(Artist.id==artist_id).all()

# ArtistGenres = ArtistGenres[0][0].split(',')
# length = len(ArtistGenres)
# for i in range(length):
#     for char in '{ }':
#         ArtistGenres[i] = ArtistGenres[i].replace(char,'')

# for item in ArtistList:
#     ArtisitDict['id'] = item[0]
#     ArtisitDict['name'] = item[1]
#     ArtisitDict['city'] = item[2]
#     ArtisitDict['state'] = item[3]
#     ArtisitDict['phone'] = item[4]
#     ArtisitDict['seeking_venue'] = item[5]
#     ArtisitDict['image_link'] = item[6]
#     ArtisitDict['facebook_link'] = item[7]
#     ArtisitDict['website_link'] = item[8]
#     ArtisitDict['seeking_description'] = item[9]
#     ArtisitDict['genres'] = ArtistGenres

#     print(ArtisitDict)


# searched = 'Music'
# venue = Venue.query
# venue = venue.filter(Venue.name.like('%' + searched + '%'))
# count = venue.count()
# venue = Venue.query.filter(func.upper(Venue.name) == searched.upper()).all()
# print(venue)
# print(venue.count())
# print(f'count is : {count}')


# result = dict()

# for v in venue:
#     result['count'] = venue.count()
#     result['data'] = venue


# print(result)


# venue_id = db.session.query(shows) (shows.venue_id)   
# artist_id = shows.query.with_entities(shows.artist_id)
# showData = dict()
# VenueData = Venue.query.with_entities(Venue.id,Venue.name).filter(Venue.id ==venue_id).all()
# ArtistData = Artist.query.with_entities(Artist.id,Artist.name,Artist.image_link).filter(Artist.id==artist_id).all()

# q = db.session.query(Artist.name,Artist.image_link).join(shows)
# q =Artist.query.join('shows.artist_id/')
# q = db.session.query(shows)
# q = shows.query.all()
# print(q)


# ven = Venue.query.join(Artist.venues).all()
# art = Artist.query.join(Venue.artists).all()


# st= db.session.query(Venue.artists).all()
# print(st)
# st2= db.session.query(Venue).join(Artist).filter(Venue.artists==Artist.venues).all()
# print(st2)

# result =select(
#      Bundle("Venue", Venue.name, Venue.id),
#      Bundle("Artist", Artist.name)
#      ).join_from(Venue, Artist)


# for row in result:
#     print(row.Venue.name)
# q = Artist.query.join(Venue,Artist.venues)

Shows = Venue.query.with_entities(Venue.id,Venue.name,Artist.id,Artist.name,Artist.image_link).join(Venue.artists).all()
showData = []
data = dict()
# for index in Shows:
#     # for tuple in index:
#         data['venue_id'] = index[0]
#         data['venue_name'] = index[1]
#         data['artist_id'] = index[2]
#         data['artist_name'] = index[3]
#         data['artist_image_link'] = index[4]
#         showData.append(data)
# print(showData)
# i = 0
# for show in Shows:
#         data = dict()
#         data['venue_id'] =show[0]
#         data['venue_name'] =show[1]
#         data['artist_id'] =show[2]
#         data['artist_name']=show[3]
#         data['artist_image_link']=show[4]
#         showData.append(data)
# print(showData)
        
# i = 0 
# while i <listLingth:
#     dict(Shows[i])
#     showData.append(Shows[i])
#     i+=1
# print(showData)
