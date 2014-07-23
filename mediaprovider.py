#################################################
#												#
#		mediaprovider module					#
#		class: MediaProvider 					#
#												#
#	Attributes:									#
#		mediaPath - absolute path to media 		#
#					rootfolder					#
#												#		
#	Methods:									#	
#		getAlbumList							#
#		getSongList								#
#		getSongInfo
#################################################

from os import path, listdir
from tagger import ID3v1
from mutagen.mp3 import MP3
import sqlite3
from operator import itemgetter

class MediaProvider:
	def __init__(self, mpath):
		if mpath != None:
			if(path.exists(mpath)):
				self.mediaPath = mpath
			else:
				print "Mediaprovider: Path %s doesn't exist" % (path.abspath(mpath))


	def getArtistList(self):
		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT DISTINCT artist from album ORDER BY artist")
		result = c.fetchall()
		
		db.close()

		return result
	

	def getAlbumList(self,artist):
		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT title,cover,id from album where artist=? ORDER BY title",(artist,))
		result = c.fetchall()
		
		db.close()
		
		return result


	def get_songs_by_album_id(self, album_id):
		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT s.title,s.length,s.filepath,s.number, a.cover FROM album a,songs s WHERE a.id=s.album AND s.album=? ORDER BY s.number",(album_id,))
		result = c.fetchall()
			
		db.close()
			
		return result

	def get_next_album_id(self,current_id,direction=1):
		### returns the id of the next album in order.
		### if direction is -1, the id of the previous album will be returned
		### wraps around album list, e.g when reaching end of list -> returns first


		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT id,artist,title FROM album ORDER BY artist,title")

		result = c.fetchall()

		nextid = 0
		for i in xrange(len(result)):
			if result[i][0]==current_id:
				#print 'aktuell: ', result[i][2]
				try:
					nextid = result[i+direction][0]
				except IndexError:
					if(direction==1):
						nextid = result[0][0]
					else:
						nextid = result[len(result)-1][0]
			
		db.close()
		
		#print result	
		return nextid

	def getSongInfo(self, filepath):
		try:
			cover = ''
			length = MP3(filepath).info.length
			id3 = ID3v1(filepath)
			for i in listdir(path.split(filepath)[0]):
				if path.splitext(i)[1] in ('.jpg','.png'): 
					cover = path.join(path.split(filepath)[0],i)
			return {'title':id3.songname, 
					'album':id3.album, 
					'artist':id3.artist, 
					'cover': cover,
					'length': length,
					'path': filepath,
					'number':id3.track}
		except IOError:
			#print 'Warning for file: ',filepath
			#print 'No ID3v1 tags available'
			return None

	def get_song_info_db(self,filepath):
		db = sqlite3.connect('library.db')
		c = db.cursor()
		c.execute('SELECT a.title, s.title, s.length, s.number, a.cover, a.artist from songs s, album a where s.album=a.id and s.filepath=?',(filepath,))
		result = c.fetchall()
		db.close()
		return {'album':result[0][0],
				'title':result[0][1],
				'length':result[0][2],
				'number':result[0][3],
				'cover':result[0][4],
				'artist':result[0][5]}
		
	def scan_media(self):
		path.walk(path.abspath(self.mediaPath),self.scan_media_walker,0)

	def scan_media_walker(self, arg, dirname, names):
		temp_album = ""
		skip = False

		db = sqlite3.connect('library.db')
		c = db.cursor()

		try:
			if path.isfile(path.join(dirname,names[0])):
				for item in names:
					if path.splitext(path.join(dirname,item))[1] not in ('.jpg','.png'):
						song_info = self.getSongInfo(path.abspath(path.join(dirname,item)))
						if song_info != None:
							#print 'adding file to database', song_info['title']

							if song_info['album'] != temp_album:
								temp_album = song_info['album']
								c.execute("SELECT id from album where title=?",(song_info['album'],))
								result = c.fetchall()
								if len(result)==0:
									c.execute("INSERT INTO album (title,artist,cover) values (?,?,?)",(song_info['album'],song_info['artist'],song_info['cover'],))
									last_id = c.lastrowid
									skip = False
								else:
									last_id = result[0][0]
									skip = True
							if not skip:
								c.execute("INSERT INTO songs (title,album,length,filepath,number) values (?,?,?,?,?)",(song_info['title'],int(last_id),song_info['length'],song_info['path'],int(song_info['number']),))

			db.commit()
			db.close()

		except IndexError:
			print 'Scanning Media: Warning: Empty folder:', dirname