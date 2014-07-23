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
from operator import itemgetter

class MediaProvider:
	def __init__(self, mpath):
		if(path.exists(mpath)):
			self.mediaPath = mpath
		else:
			print "Path %s doesn't exist" % (path.abspath(mpath))

	def getAlbumList(self):
		self._albumList = []
		#return listdir(self.mediaPath)
		path.walk(path.abspath(self.mediaPath),self.fillAlbumList,0)
		
		return sorted(self._albumList,key=itemgetter('artist','album'))

	def getSongList(self, artist, album):
		self._songList = []
		albumPath = '/'.join([self.mediaPath,artist,album])
		path.walk(path.abspath(albumPath), self.fillSongList,0)

		if len(self._songList)>0:
			return sorted(self._songList,key=itemgetter('path'))
		else:
			return []

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
					'length': length}
		except IOError:
			print 'Warning for file: ',filepath
			print 'No ID3v1 tags available, using filenames names instead'
			return {'title':path.basename(filepath), 
					'album':path.basename(path.dirname(path.split(filepath)[0])), 
					'artist':path.basename(path.dirname(filepath)),
					'cover':'',
					'length': ''}

	def fillAlbumList(self, arg, dirname, names):
		try:
			if path.isfile(path.join(dirname,names[0])):		#file level
				artist = path.basename(path.dirname(dirname))
				album = path.basename(path.dirname(path.join(dirname,names[0])))
				cover = ''

				for i in names:
					if path.splitext(path.join(dirname,i))[1] in ('.jpg','.png'):
						cover = path.join(dirname,i)
				
				self._albumList.append({'artist':artist,'album':album,'cover':cover})
		except IndexError:
			print 'Warning: Empty folder:', dirname

	def fillSongList(self, arg, dirname, names):
		for i in names:
			if path.splitext(path.join(dirname,i))[1] not in ('.jpg','.png'):
				songpath = path.join(dirname,i)
				info = self.getSongInfo(songpath)
				self._songList.append({'title':info['title'], 'path':songpath, 'length':info['length']})
