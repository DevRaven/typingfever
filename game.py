import pygame, sys, json, ctypes, random, linecache
from pygame.locals import *
from random import randrange
user32 = ctypes.windll.user32


#setup wordcount (used to gen max random number later to fetch words)
file = open("./resources/data/words.txt", "r")
line_count = 0
for line in file:
    if line != "\n":
        line_count += 1
file.close()

#check resolution settings
f = open("./resources/data/settings.json", "r")
data = json.load(f)
f.close()
if data['resolution'] == 0:
	data['resolution'] = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
	f = open("./resources/data/settings.json", "w")
	json.dump(data, f)
	f.close()

#start game engine & clock
mainClock = pygame.time.Clock()
pygame.init()

#set window settings
pygame.display.set_caption('Typing Fever')
screensize = data['resolution'][0], data['resolution'][1]
if data['fullscreen'] == "yes":
	screen = pygame.display.set_mode((screensize),FULLSCREEN,32)
else:
	screen = pygame.display.set_mode((screensize),0,32)
pygame.mouse.set_visible(0)
bg = pygame.image.load("./resources/images/bg.jpg")

#set sounds
menusound = pygame.mixer.Sound('./resources/sounds/menu.wav')
menusound.set_volume(int(data['sfx'])/100)
hitsound = pygame.mixer.Sound('./resources/sounds/hit.wav')
hitsound.set_volume(int(data['sfx'])/100)
killsound = pygame.mixer.Sound('./resources/sounds/kill.wav')
killsound.set_volume(int(data['sfx'])/100)
backgroundmusic = pygame.mixer.music.load('./resources/sounds/bgm.mp3')
pygame.mixer.music.set_volume(int(data['bgm'])/100)
pygame.mixer.music.play(-1)


#set font
def font(size):
	return pygame.font.Font("./resources/fonts/RobotCrush.ttf", size)

#text drawer
def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect(center=(x, y))
	surface.blit(textobj, textrect)

#create our starting menu screen
def startMenu(selected):
	while True:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		#title
		draw_text('TYPING FEVER', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
		#menu handler
		if selected == 0:
			draw_text('>S T A R T', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/2.8))
			draw_text('LEADERBOARDS', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.15))
			draw_text('OPTIONS', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.7))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
		elif selected == 1:
			draw_text('START', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.8))
			draw_text('>L E A D E R B O A R D S', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/2.15))
			draw_text('OPTIONS', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.7))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
		elif selected == 2:
			draw_text('START', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.8))
			draw_text('LEADERBOARDS', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.15))
			draw_text('>O P T I O N S', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.7))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
		elif selected == 3:
			draw_text('START', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.8))
			draw_text('LEADERBOARDS', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.15))
			draw_text('OPTIONS', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.7))
			draw_text('>Q U I T', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.4))
		#event handler
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_SPACE:
					if selected == 0:
						menusound.play()
						start(0)
					elif selected == 1:
						menusound.play()
						leaderboards(0)
					elif selected == 2:
						menusound.play()
						options(0)
					elif selected == 3:
						pygame.quit()
						sys.exit()
				elif event.key == K_DOWN or event.key == K_s:
					if selected < 3:
						menusound.play()
						selected = selected + 1
					elif selected == 3:
						menusound.play()
						selected = 0
				elif event.key == K_UP or event.key == K_w:
					if selected > 0:
						menusound.play()
						selected = selected - 1
					elif selected == 0:
						menusound.play()
						selected = 3
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)

def options(selected):
	#setup all variables and fetch data from json file
	active = True
	f = open("./resources/data/settings.json", "r")
	data = json.load(f)
	bgmval = data['bgm']
	sfxval = data['sfx']
	fullscreenval = data['fullscreen']
	resolutions = ["1920x1080", "1600x900", "1366x768", "1280x720", "1920x1200", "1680x1050", "1440x900", "1024x768"]
	currentres = str(data['resolution'][0])+"x"+str(data['resolution'][1])
	resindex = 0
	for i in range(len(resolutions)):
		if resolutions[i] == currentres:
			resindex = i
			break
	while active:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		#title
		draw_text('OPTIONS', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
		if selected == 0:
			draw_text('>B G M: '+bgmval, font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/3.1))
			draw_text('SFX: '+sfxval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.4))
			draw_text('FULLSCREEN: '+fullscreenval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('RESOLUTION: '+resolutions[resindex], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
			draw_text('SAVE AND QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.2))
		elif selected == 1:
			draw_text('BGM: '+bgmval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3.1))
			draw_text('>S F X: '+sfxval, font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/2.4))
			draw_text('FULLSCREEN: '+fullscreenval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('RESOLUTION: '+resolutions[resindex], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
			draw_text('SAVE AND QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.2))
		elif selected == 2:
			draw_text('BGM: '+bgmval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3.1))
			draw_text('SFX: '+sfxval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.4))
			draw_text('>F U L L S C R E E N: '+fullscreenval, font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('RESOLUTION: '+resolutions[resindex], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
			draw_text('SAVE AND QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.2))
		elif selected == 3:
			draw_text('BGM: '+bgmval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3.1))
			draw_text('SFX: '+sfxval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.4))
			draw_text('FULLSCREEN: '+fullscreenval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('>R E S O L U T I O N: '+resolutions[resindex], font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.65))
			draw_text('SAVE AND QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.2))
		elif selected == 4:
			draw_text('BGM: '+bgmval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3.1))
			draw_text('SFX: '+sfxval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.4))
			draw_text('FULLSCREEN: '+fullscreenval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('RESOLUTION: '+resolutions[resindex], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
			draw_text('>S A V E  A N D   Q U I T', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.4))
			draw_text('QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.2))
		elif selected == 5:
			draw_text('BGM: '+bgmval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3.1))
			draw_text('SFX: '+sfxval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.4))
			draw_text('FULLSCREEN: '+fullscreenval, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('RESOLUTION: '+resolutions[resindex], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
			draw_text('SAVE AND QUIT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.4))
			draw_text('>Q U I T', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.2))
		#event handler
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_SPACE:
					if selected == 4:
						menusound.play()
						data['bgm'] = bgmval
						data['sfx'] = sfxval
						newres = list(map(int, resolutions[resindex].split("x")))
						f = open("./resources/data/settings.json", "w")
						json.dump(data, f)
						f.close()
						if fullscreenval != data['fullscreen']:
							restart(0, fullscreenval, newres)
							active = False
							startMenu(0)
						elif newres != data['resolution']:
							restart(0, fullscreenval, newres)
							active = False
							startMenu(0)
						pygame.mixer.music.set_volume(int(data['bgm'])/100)
						menusound.set_volume(int(data['sfx'])/100)
						hitsound.set_volume(int(data['sfx'])/100)
						killsound.set_volume(int(data['sfx'])/100)
						active = False
						startMenu(0)
					elif selected == 5:
						menusound.play()
						active = False
						startMenu(0)
				elif event.key == K_RIGHT or event.key == K_d:
					if selected == 0:
						if int(bgmval) < 100:
							bgmval = str(int(bgmval) + 10)
							pygame.mixer.music.set_volume(int(bgmval)/100)
							menusound.play()
					elif selected == 1:
						if int(sfxval) < 100:
							sfxval = str(int(sfxval) + 10)
							menusound.set_volume(int(sfxval)/100)
							hitsound.set_volume(int(sfxval)/100)
							killsound.set_volume(int(sfxval)/100)
							menusound.play()
					elif selected == 2:
						if fullscreenval == "yes":
							menusound.play()
							fullscreenval = "no"
						elif fullscreenval == "no":
							menusound.play()
							fullscreenval = "yes"
					elif selected == 3:
						if resindex < len(resolutions)-1:
							menusound.play()
							resindex = resindex +1
				elif event.key == K_LEFT or event.key == K_a:
					if selected == 0:
						if int(bgmval) > 0:
							bgmval = str(int(bgmval) - 10)
							pygame.mixer.music.set_volume(int(bgmval)/100)
							menusound.play()
					elif selected == 1:
						if int(sfxval) > 0:
							sfxval = str(int(sfxval) - 10)
							menusound.set_volume(int(sfxval)/100)
							hitsound.set_volume(int(sfxval)/100)
							killsound.set_volume(int(sfxval)/100)
							menusound.play()
					elif selected == 2:
						if fullscreenval == "yes":
							menusound.play()
							fullscreenval = "no"
						elif fullscreenval == "no":
							menusound.play()
							fullscreenval = "yes"
					elif selected == 3:
						if resindex > 0:
							menusound.play()
							resindex = resindex -1
				elif event.key == K_DOWN or event.key == K_s:
					if selected < 5:
						menusound.play()
						selected = selected + 1
					elif selected == 5:
						menusound.play()
						selected = 0
				elif event.key == K_UP or event.key == K_w:
					if selected > 0:
						menusound.play()
						selected = selected - 1
					elif selected == 0:
						menusound.play()
						selected = 5
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)

def restart(selected, fullscreenval, newres):
	#define vars
	active = True
	while active:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		draw_text('OPTIONS', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
		draw_text('SOME CHANGES NEED A RESTART TO TAKE EFFECT', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3.1))
		if selected == 0:
			draw_text('>O K A Y<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('UNDO CHANGES', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
		if selected == 1:
			draw_text('OKAY', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('>U N D O  C H A N G E S<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.65))
		#event handler
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_SPACE:
					if selected == 0:
						menusound.play()
						f = open("./resources/data/settings.json", "r")
						data = json.load(f)
						f.close()
						data['fullscreen'] = fullscreenval
						data['resolution'] = newres
						f = open("./resources/data/settings.json", "w")
						json.dump(data, f)
						f.close()
						active = False
						startMenu(0)
					elif selected == 1:
						menusound.play()
						active = False
						startMenu(0)
				elif event.key == K_DOWN or event.key == K_s:
					if selected < 1:
						menusound.play()
						selected = selected + 1
					elif selected == 1:
						menusound.play()
						selected = 0
				elif event.key == K_UP or event.key == K_w:
					if selected > 0:
						menusound.play()
						selected = selected - 1
					elif selected == 0:
						menusound.play()
						selected = 1
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)

def start(selected):
	#define vars
	active = True
	difficulties = ['E A S Y', 'M E D I U M', 'H A R D', 'I M P O S S I B L E', 'easy', 'medium', 'hard', 'impossible']
	index = 0
	while active:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		draw_text('DIFFICULTY', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
		if selected == 0:
			draw_text('>'+difficulties[index]+'<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('BACK', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.65))
		elif selected == 1:
			draw_text(difficulties[index+4], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
			draw_text('>B A C K<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.65))
		#event handler
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_SPACE:
					if selected == 0:
						menusound.play()
						active = False
						play(index)
					elif selected == 1:
						menusound.play()
						active = False
						startMenu(0)
				elif event.key == K_RIGHT or event.key == K_d:
					if selected == 0:
						if index < 3:
							menusound.play()
							index = index +1
						elif index == 3:
							menusound.play()
							index = 0
				elif event.key == K_LEFT or event.key == K_a:
					if selected == 0:
						if index > 0:
							menusound.play()
							index = index - 1
						elif index == 0:
							menusound.play()
							index = 3
				elif event.key == K_DOWN or event.key == K_s:
					if selected < 1:
						menusound.play()
						selected = selected + 1
					elif selected == 1:
						menusound.play()
						selected = 0
				elif event.key == K_UP or event.key == K_w:
					if selected > 0:
						menusound.play()
						selected = selected - 1
					elif selected == 0:
						menusound.play()
						selected = 1
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)

def spawn():
	#return array consisting of random word from file, random color as well as random x and y coordinates
	word = linecache.getline('./resources/data/words.txt', random.randint(1, line_count)).rstrip('\n')
	return [pygame.font.Font("./resources/fonts/Inlanders.otf", 60).render(word, 1, (randrange(255),randrange(255),255)), randrange(screensize[0]-500), (randrange(800)*-1), word]

def play(difficulty):
	#define vars
	active = True
	enemies = []
	health = 3
	score = 0
	typed = ""
	spawnspeed = int(10000/(int(difficulty)+1))
	scrollspeed = 1
	#create event timer
	SPAWNEVENT = pygame.USEREVENT+1
	pygame.time.set_timer(SPAWNEVENT, spawnspeed)
	enemies.append(spawn())
	while active:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		#draw stats and heads-up display
		draw_text("Health: "+str(health), font(60), (255,51,0), screen, (screensize[0]/10), (screensize[1]/8))
		draw_text("Score: "+str(score), font(60), (255,51,0), screen, (screensize[0]/10), (screensize[1]/15))
		draw_text(">"+typed, font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.1))
		#animate enemies
		for i in range(len(enemies)):
			screen.blit(enemies[i][0], (enemies[i][1],enemies[i][2]))
			enemies[i][2]+=scrollspeed
			#check if enemy passed screen
			if enemies[i][2] > screensize[1]+100:
				#if enemy passed screen, reset speed, clear all enemies, play hit sound and remove health
				hitsound.play()
				enemies = []
				spawnspeed = int(10000/(int(difficulty)+1))
				scrollspeed = 1
				health -= 1
				break
		#check if game lost
		if health <= -1:
			#game lost, switch to save score menu and pass final score
			active = False
			savescore(score, difficulty)
		#event handler
		for event in pygame.event.get():
			if event.type == SPAWNEVENT:
				enemies.append(spawn())
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					active = False
					startMenu(0)
				elif event.key == K_RETURN:
					#check if typed word is an enemy
					for n in range(len(enemies)):
						if typed == enemies[n][3]:
							#remove enemy, increase spawn and scroll speeds, add score and play kill sound
							killsound.play()
							enemies.pop(n)
							score += 100
							spawnspeed -= randrange(10)
							scrollspeed += ((difficulty/10000)+0.05)
							pygame.time.set_timer(SPAWNEVENT, spawnspeed)
							break
					#reset typed word
					typed = ""
				elif event.key == K_BACKSPACE:
					typed = typed[:-1]
				else:
					typed += event.unicode
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)

def savescore(score, difficulty):
	active = True
	f = open("./resources/data/scores.json", "r")
	data = json.load(f)
	f.close()
	pushDownAmount = 0
	difficulties = ['easy', 'medium', 'hard', 'impossible']
	selected = 0
	newscore = False
	setname = False
	name = ""
	for obj in data[difficulties[difficulty]]:
		if score > data[difficulties[difficulty]][obj]['score']:
			pushDownAmount = int(obj)
			break
	while active:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		#check if new high-score
		if pushDownAmount == 0:
			draw_text('GAME OVER', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
			draw_text('>B A C K<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.95))
		else:
			draw_text('GAME OVER', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
			draw_text('NEW HIGH-SCORE!', font(80), (255,255,255), screen, (screensize[0]/2), (screensize[1]/4))
			draw_text('ENTER YOUR NAME', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.3))
			if selected == 0:
				draw_text('>'+name, font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.95))
				draw_text('SAVE', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.75))
			elif selected == 1:
				draw_text(name, font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.95))
				draw_text('>S A V E<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.75))
			newscore = True
		#event handler
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_SPACE:
					if newscore == False:
						active = False
						startMenu(0)
					else:
						if selected == 0:
							setname = True
						if selected == 1:
							pushDownAmount = int(pushDownAmount)
							if pushDownAmount == 1:
								data[difficulties[difficulty]]["5"]['score'] = data[difficulties[difficulty]]["4"]['score']
								data[difficulties[difficulty]]["5"]['name'] = data[difficulties[difficulty]]["4"]['name']
								data[difficulties[difficulty]]["4"]['score'] = data[difficulties[difficulty]]["3"]['score']
								data[difficulties[difficulty]]["4"]['name'] = data[difficulties[difficulty]]["3"]['name']
								data[difficulties[difficulty]]["3"]['score'] = data[difficulties[difficulty]]["2"]['score']
								data[difficulties[difficulty]]["3"]['name'] = data[difficulties[difficulty]]["2"]['name']
								data[difficulties[difficulty]]["2"]['score'] = data[difficulties[difficulty]]["1"]['score']
								data[difficulties[difficulty]]["2"]['name'] = data[difficulties[difficulty]]["1"]['name']
								data[difficulties[difficulty]]["1"]['score'] = score
								data[difficulties[difficulty]]["1"]['name'] = name
							elif pushDownAmount == 2:
								data[difficulties[difficulty]]["5"]['score'] = data[difficulties[difficulty]]["4"]['score']
								data[difficulties[difficulty]]["5"]['name'] = data[difficulties[difficulty]]["4"]['name']
								data[difficulties[difficulty]]["4"]['score'] = data[difficulties[difficulty]]["3"]['score']
								data[difficulties[difficulty]]["4"]['name'] = data[difficulties[difficulty]]["3"]['name']
								data[difficulties[difficulty]]["3"]['score'] = data[difficulties[difficulty]]["2"]['score']
								data[difficulties[difficulty]]["3"]['name'] = data[difficulties[difficulty]]["2"]['name']
								data[difficulties[difficulty]]["2"]['score'] = score
								data[difficulties[difficulty]]["2"]['name'] = name
							elif pushDownAmount == 3:
								data[difficulties[difficulty]]["5"]['score'] = data[difficulties[difficulty]]["4"]['score']
								data[difficulties[difficulty]]["5"]['name'] = data[difficulties[difficulty]]["4"]['name']
								data[difficulties[difficulty]]["4"]['score'] = data[difficulties[difficulty]]["3"]['score']
								data[difficulties[difficulty]]["4"]['name'] = data[difficulties[difficulty]]["3"]['name']
								data[difficulties[difficulty]]["3"]['score'] = score
								data[difficulties[difficulty]]["3"]['name'] = name
							elif pushDownAmount == 4:
								data[difficulties[difficulty]]["5"]['score'] = data[difficulties[difficulty]]["4"]['score']
								data[difficulties[difficulty]]["5"]['name'] = data[difficulties[difficulty]]["4"]['name']
								data[difficulties[difficulty]]["4"]['score'] = score
								data[difficulties[difficulty]]["4"]['name'] = name
							elif pushDownAmount == 4:
								data[difficulties[difficulty]]["5"]['score'] = score
								data[difficulties[difficulty]]["5"]['name'] = name
							f = open("./resources/data/scores.json", "w")
							json.dump(data, f)
							f.close()
							setname = False
							active = False
							startMenu(0)
				elif event.key == K_DOWN:
					if selected < 1:
						menusound.play()
						selected = selected + 1
					elif selected == 1:
						menusound.play()
						selected = 0
				elif event.key == K_UP:
					if selected > 0:
						menusound.play()
						selected = selected - 1
					elif selected == 0:
						menusound.play()
						selected = 1
				elif event.key == K_BACKSPACE:
					name = name[:-1]
				else:
					if len(name) < 3:
						name += event.unicode
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)

		
def leaderboards(selected):
	active = True
	f = open("./resources/data/scores.json", "r")
	data = json.load(f)
	f.close()
	difficulties = ['E A S Y', 'M E D I U M', 'H A R D', 'I M P O S S I B L E', 'easy', 'medium', 'hard', 'impossible']
	difficultiesNonText = ['easy', 'medium', 'hard', 'impossible']
	index = 0
	while active:
		#create background
		screen.fill((0,0,0))
		screen.blit(pygame.transform.scale(bg, screensize), (0, 0))
		#title and table key setup
		draw_text('LEADRBOARDS', font(150), (255,255,255), screen, (screensize[0]/2), (screensize[1]/8))
		draw_text('RANK', font(80), (255,255,255), screen, (screensize[0]/3), (screensize[1]/4))
		draw_text('NAME', font(80), (255,255,255), screen, (screensize[0]/2), (screensize[1]/4))
		draw_text('SCORE', font(80), (255,255,255), screen, (screensize[0]/1.5), (screensize[1]/4))
		#display scores
		draw_text('1st', font(60), (255,255,255), screen, (screensize[0]/3), (screensize[1]/3))
		draw_text(data[difficultiesNonText[index]]["1"]["name"], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/3))
		draw_text(str(data[difficultiesNonText[index]]["1"]["score"]), font(60), (255,255,255), screen, (screensize[0]/1.5), (screensize[1]/3))
		draw_text('2nd', font(60), (255,255,255), screen, (screensize[0]/3), (screensize[1]/2.4))
		draw_text(data[difficultiesNonText[index]]["2"]["name"], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2.4))
		draw_text(str(data[difficultiesNonText[index]]["2"]["score"]), font(60), (255,255,255), screen, (screensize[0]/1.5), (screensize[1]/2.4))
		draw_text('3rd', font(60), (255,255,255), screen, (screensize[0]/3), (screensize[1]/2))
		draw_text(data[difficultiesNonText[index]]["3"]["name"], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/2))
		draw_text(str(data[difficultiesNonText[index]]["3"]["score"]), font(60), (255,255,255), screen, (screensize[0]/1.5), (screensize[1]/2))
		draw_text('4th', font(60), (255,255,255), screen, (screensize[0]/3), (screensize[1]/1.7))
		draw_text(data[difficultiesNonText[index]]["4"]["name"], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.7))
		draw_text(str(data[difficultiesNonText[index]]["4"]["score"]), font(60), (255,255,255), screen, (screensize[0]/1.5), (screensize[1]/1.7))
		draw_text('5th', font(60), (255,255,255), screen, (screensize[0]/3), (screensize[1]/1.5))
		draw_text(data[difficultiesNonText[index]]["5"]["name"], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.5))
		draw_text(str(data[difficultiesNonText[index]]["5"]["score"]), font(60), (255,255,255), screen, (screensize[0]/1.5), (screensize[1]/1.5))

		#change mode scores
		if selected == 0:
			draw_text('>'+difficulties[index]+'<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.3))
			draw_text('BACK', font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.2))
		elif selected == 1:
			draw_text(difficulties[index+4], font(60), (255,255,255), screen, (screensize[0]/2), (screensize[1]/1.3))
			draw_text('>B A C K<', font(60), (255,51,0), screen, (screensize[0]/2), (screensize[1]/1.2))
		#event handler
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN or event.key == K_SPACE:
					if selected == 1:
						menusound.play()
						active = False
						startMenu(0)
				elif event.key == K_RIGHT or event.key == K_d:
					if selected == 0:
						if index < 3:
							menusound.play()
							index = index +1
						elif index == 3:
							menusound.play()
							index = 0
				elif event.key == K_LEFT or event.key == K_a:
					if selected == 0:
						if index > 0:
							menusound.play()
							index = index - 1
						elif index == 0:
							menusound.play()
							index = 3
				elif event.key == K_DOWN or event.key == K_s:
					if selected < 1:
						menusound.play()
						selected = selected + 1
					elif selected == 1:
						menusound.play()
						selected = 0
				elif event.key == K_UP or event.key == K_w:
					if selected > 0:
						menusound.play()
						selected = selected - 1
					elif selected == 0:
						menusound.play()
						selected = 1
		#gametick and display updater
		pygame.display.update()
		mainClock.tick(60)
		
#start game
startMenu(0)
