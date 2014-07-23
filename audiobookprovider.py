from os import path, listdir
from tagger import ID3v1
from mutagen.mp3 import MP3
from kivy.storage.jsonstore import JsonStore
import sqlite3
from operator import itemgetter

class AudiobookProvider:
	def __init__(self, mpath):
		if mpath != None:
			if(path.exists(mpath)):
				self.mediaPath = mpath
			else:
				print "Path %s doesn't exist" % (path.abspath(mpath))
	
	def getAudiobookList(self):
		_booklist = []

		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT a.id,a.title,a.author,a.cover,a.length, a.progress_pos, a.progress_part from audiobook a")

		result = []

		for row in c.fetchall():
			c2 = db.cursor()
			length = row[4]

			if row[6]>1:
				c2.execute("SELECT sum(length) FROM audiobookfiles where book=? AND number<?", (row[0],row[6],))
				pos = c2.fetchone()[0] + row[5]
			else:
				pos = row[5]

			row += (pos,)

			result.append(row)

		db.close()

		return result


	def get_book(self,id):
		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT title,author,cover,length,progress_part,progress_pos FROM audiobook WHERE id=?",(id,))
		audiobook_info = c.fetchall()

		c.execute("SELECT number,title,length,filepath FROM audiobookfiles WHERE book=? ORDER BY number",(id,))
		audiobook_files = c.fetchall()

		db.close()

		return {'info':{
						'title':audiobook_info[0][0],
						'author':audiobook_info[0][1],
						'cover':audiobook_info[0][2],
						'length':audiobook_info[0][3],
						'progress_part':audiobook_info[0][4],
						'progress_pos':audiobook_info[0][5]},
							'files':audiobook_files
							}
		


	def get_progress(self, id, number):
		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT sum(length) FROM audiobookfiles where book=? AND number<?", (id,number))

		result = c.fetchall()

		db.close()
		print 'DFSDFDSFSDF',number
		return result[0][0]


	def scanAudiobooks(self):
		self._book_files = []
		self._book_cover = ''

		db = sqlite3.connect('library.db')
		c = db.cursor()

		for book in listdir(self.mediaPath):
			if path.isdir(path.join(self.mediaPath,book)):
				print 'Found: ', book

				c.execute("SELECT * FROM audiobook where foldername=?", (book,))
				if len(c.fetchall()) == 0:
					self._book_files = []
					self._book_cover = ''
					self.length = 0
					c.execute("INSERT INTO audiobook (title, foldername) values (?,?)",(book, book,))
					rowid = c.lastrowid
					print 'Inserted book: %s with ID %i' % (book, rowid)

					path.walk(path.abspath(path.join(self.mediaPath,book)),self.scanAudiobooks_walker,id)
					firstfile = True
					i=1
					for bookfile in sorted(self._book_files, key=itemgetter('filepath')):
						values = (rowid,bookfile['title'],bookfile['filepath'],bookfile['length'],i,)
						c.execute("INSERT INTO audiobookfiles (book,title,filepath,length,number) values (?,?,?,?,?)", values)
						i = i+1

					c.execute("Update audiobook SET title=?, author=?, cover=?, length=?, progress_part=? where id=?", (self._book_files[0]['booktitle'],self._book_files[0]['author'],self._book_cover,self.length,1,rowid,))
		db.commit()
		db.close()

	def scanAudiobooks_walker(self, arg, dirname, names):
		try:
			if path.isfile(path.join(dirname,names[0])):		#file level

				for i in names:
					if path.splitext(path.join(dirname,i))[1] in ('.jpg','.png'):
						if self._book_cover == '':
							self._book_cover = path.join(dirname,i)

					elif path.splitext(path.join(dirname,i))[1] in ('.mp3','.aac'):
						id3 = ID3v1(path.join(dirname,i))
						length = MP3(path.join(dirname,i)).info.length
						self._book_files.append({'author':id3.artist,'booktitle':id3.album,'title':id3.songname,'filepath':path.join(dirname,i),'length':length,'number':id3.track})
						self.length += length
				
		except IndexError:
			print 'Warning: Empty folder:', dirname

	def get_file_info(self,filepath):
		db = sqlite3.connect('library.db')
		c = db.cursor()

		c.execute("SELECT a.title, a.author, a.cover from audiobook a, audiobookfiles f where f.filepath=? AND a.id=f.book",(filepath,))
		result = c.fetchall()

		db.close()

		return {'title':result[0][0],'author':result[0][1],'cover':result[0][2]}
	
	# def get_info_from_file(self,filepath):
	# 	store = JsonStore(path.join(self.mediaPath,'library.json'))
		
	# 	for book in store.keys():
	# 		if filepath in store[book]['files']:
	# 			print 'gefunden:', book
	# 			return {'author':store[book]['author'],'title':store[book]['title'], 'cover':store[book]['cover']}

	# 	#except IOError:
	# 	#	print 'Warning for file: ',filepath