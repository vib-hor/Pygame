import pygame as pg
import numpy as np
from settings import *
from random import choice, randrange
from os import path
from math import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game		
		self.image = pg.transform.scale(self.game.player_img,(60,60))#self.game.player_img
		#self.image = pg.transform.scale(game.mob_img, (180, 130))
		#self.image.set_colorkey(BLACK)
		self.radius = 50
		
		self.image_orig = self.image
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.bottom = HEIGHT 
		self.speedx = 0
		self.rot_speed = ROT_SPEED
		self.rot = 0
		self.direction = vec(120,0)
		self.arrow_tip = vec(121, HEIGHT-128+87) - vec(self.rect.center)
		self.arrow_butt = vec(27, HEIGHT-128+87) - vec(self.rect.center)
		pg.draw.circle(self.image_orig, RED, self.rect.center, self.radius)
		
		
	
	def rotated_vec(self, angle, vec_i):
		theta = radians(angle) 
		new_vec = np.matrix(((cos(theta),-sin(theta)),(sin(theta), cos(theta)))) * np.transpose(np.matrix(((vec_i.x, vec_i.y))))
		return vec(new_vec[0], new_vec[1])

	def rotate(self, counter):
		self.rot_speed = ROT_SPEED
		if self.rot  > 180 and self.rot < 190:
			#self.rot_speed = 0
			self.rot = 180
		if self.rot  < 325 and self.rot > 180:
			#self.rot_speed = 0
			self.rot = 325
		self.rot = (self.rot + self.rot_speed * counter) % 360
 		new_image = pg.transform.rotate(self.image_orig, self.rot)
		old_pivot = self.rect.center
		self.image = new_image
		self.rect = self.image.get_rect()
		self.rect.center = old_pivot
		self.arrow_tip = self.rotated_vec(self.rot ,self.arrow_tip)
		self.arrow_butt = self.rotated_vec(self.rot ,self.arrow_butt)


	def shoot(self):
		arrow = Arrow(self.game, self.arrow_butt, self.arrow_tip, self.rot )
		self.game.all_sprites.add(arrow)
		self.game.arrows.add(arrow)
		arrow.rotate((self.rot-13))
		#self.image = pg.transform.scale(self.game.player_img1,(60,60))


		

	def rotPoint(self, point, axis, ang):
		""" Orbit. calcs the new loc for a point that rotates a given num of degrees around an axis point,
		+clockwise, -anticlockwise -> tuple x,y
		"""
		x, y = point[0] - axis[0], point[1] - axis[1]
		radius = sqrt(x*x + y*y) # get the distance between points

		RAng = radians(ang)       # convert ang to radians.


		h = axis[0] + ( radius * cos(RAng) )
		v = axis[1] + ( radius * sin(RAng) )
		return h, v

	def update(self):
		self.speedx = 0
		keys = pg.key.get_pressed()
		"""if keys[pg.K_a]:
			self.speedx = -PLAYER_SPEED
		if keys[pg.K_d]:
			self.speedx = PLAYER_SPEED"""
		if keys[pg.K_a]:
			#self.rect.center = self.rotPoint(self.rect.center, (27,HEIGHT -128+87), 5)
			self.rotate(1)		# 1 for upwards
		if keys[pg.K_d]:
			#self.rect.center = self.rotPoint(self.rect.center, (27,HEIGHT -128+87), -5)
			self.rotate(-1)
		
		self.rect.x += self.speedx
		pg.draw.line(self.game.screen, RED, (100,100), (0, 0))
		"""if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH"""

class Mob(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.factor =  2/3.0
		self.frame = 0
		self.image = pg.transform.scale(self.game.mob_img[0] ,(int(self.factor*180), int(self.factor*130)))#self.game.player_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.spawn()
		self.radius = 50*self.factor
		self.rage = False
		if self.ch == game.mob_img1:
			self.rage = True
		#pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		

	def update(self):
		self.rect.x += self.speedx
		if self.rect.x > WIDTH:
			self.spawn()	
		self.frame +=1
		self.image = pg.transform.scale(self.ch[self.frame%16 / 4] , (int(self.factor*180), int(self.factor*130)))

	def spawn(self):
		self.rect.x,self.rect.y = (randrange(-200, -100),randrange(0,4*HEIGHT/7) )
		self.speedx = randrange(2,MOB_SPEED)
		imgs = [self.game.mob_img, self.game.mob_img1]
		self.ch = choice(imgs)
		self.image = pg.transform.scale(self.ch[0] , (int(self.factor*180), int(self.factor*130)))

class Arrow(pg.sprite.Sprite):
	def __init__(self, game, vec_butt, vec_tip, rot):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.transform.scale(self.game.arrow_img,(40,40))#self.game.arrow_img
		self.image_orig = self.image
		#self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20 * 80/128
		self.pos = vec(self.game.player.rect.center)
		vec_i = vec_butt + self.pos
		self.vec_butt = vec_butt
		self.vec_tip = vec_tip
		self.rect.bottom = vec_i.y
		self.rect.centerx = vec_i.x 
		self.acc = vec(0, GRAVITY)
		d = (vec_tip - vec_butt) 
		#self.vel = d * ARROW_SPEED/ sqrt(d.x*d.x + d.y*d.y)
		theta = radians(rot+ARROW_ANGLE)
		self.vel = vec(cos(theta), -sin(theta)) * ARROW_SPEED
		self.rot = rot 

	
	def rotate(self, angle):
		self.rot = angle 
		new_image = pg.transform.rotate(self.image_orig, self.rot)
		old_pivot = self.rect.center
		self.image = new_image
		self.rect = self.image.get_rect()
		self.rect.center = old_pivot
		pg.draw.circle(self.image_orig, RED, self.rect.center, self.radius)
		
	def update(self):
		"""self.vel += self.acc 
		self.pos += self.vel + 0.5 * self.acc
		self.rotate(self.rot + atan(self.vel.y/self.vel.x))"""
		self.pos += self.vel
		#self.pos += self.vel
		self.rect.center = self.pos


'''import pygame as pg
import numpy as np
from settings import *
from random import choice, randrange
from os import path
from math import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game		
		self.image = pg.transform.scale(self.game.player_img,(60,60))#self.game.player_img
		#self.image = pg.transform.scale(game.mob_img, (180, 130))
		#self.image.set_colorkey(BLACK)
		self.radius = 50
		
		self.image_orig = self.image
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.bottom = HEIGHT 
		self.speedx = 0
		self.rot_speed = ROT_SPEED
		self.rot = 0
		self.direction = vec(120,0)
		self.arrow_tip = vec(121, HEIGHT-128+87) - vec(self.rect.center)
		self.arrow_butt = vec(27, HEIGHT-128+87) - vec(self.rect.center)
		#pg.draw.circle(self.image_orig, RED, self.rect.center, self.radius)
		self.arrow = Arrow(self, self.game, self.arrow_butt, self.arrow_tip, self.rot-13)
		self.add_arrow(self.arrow)
		
		
	
	def rotated_vec(self, angle, vec_i):
		theta = radians(angle) 
		new_vec = np.matrix(((cos(theta),-sin(theta)),(sin(theta), cos(theta)))) * np.transpose(np.matrix(((vec_i.x, vec_i.y))))
		return vec(new_vec[0], new_vec[1])

	def rotate(self, counter):
		self.rot_speed = ROT_SPEED
		if self.rot  > 180 and self.rot < 190:
			#self.rot_speed = 0
			self.rot = 180
		if self.rot  < 325 and self.rot > 180:
			#self.rot_speed = 0
			self.rot = 325
		self.rot = (self.rot + self.rot_speed * counter) % 360
 		new_image = pg.transform.rotate(self.image_orig, self.rot)
		old_pivot = self.rect.center
		self.image = new_image
		self.rect = self.image.get_rect()
		self.rect.center = old_pivot
		self.arrow_tip = self.rotated_vec(self.rot ,self.arrow_tip)
		self.arrow_butt = self.rotated_vec(self.rot ,self.arrow_butt)


	def shoot(self):
		self.arrow.vel = vec(cos(radians(self.arrow.rot)), -sin(radians(self.arrow.theta))) * ARROW_SPEED		
		self.arrow = Arrow(self, self.game, self.arrow_butt, self.arrow_tip, self.rot)
		self.add_arrow(self.arrow)
		self.arrow.rotate((self.rot))


	def add_arrow(self, arrow):
		self.game.all_sprites.add(arrow)
		self.game.arrows.add(arrow)
		

	def rotPoint(self, point, axis, ang):
		""" Orbit. calcs the new loc for a point that rotates a given num of degrees around an axis point,
		+clockwise, -anticlockwise -> tuple x,y
		"""
		x, y = point[0] - axis[0], point[1] - axis[1]
		radius = sqrt(x*x + y*y) # get the distance between points

		RAng = radians(ang)       # convert ang to radians.


		h = axis[0] + ( radius * cos(RAng) )
		v = axis[1] + ( radius * sin(RAng) )
		return h, v

	def update(self):
		self.speedx = 0
		keys = pg.key.get_pressed()
		"""if keys[pg.K_a]:
			self.speedx = -PLAYER_SPEED
		if keys[pg.K_d]:
			self.speedx = PLAYER_SPEED"""
		if keys[pg.K_a]:
			#self.rect.center = self.rotPoint(self.rect.center, (27,HEIGHT -128+87), 5)
			self.rotate(1)		# 1 for upwards
		if keys[pg.K_d]:
			#self.rect.center = self.rotPoint(self.rect.center, (27,HEIGHT -128+87), -5)
			self.rotate(-1)
		
		self.rect.x += self.speedx
		self.arrow.rotate((self.rot))
		"""if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH"""

class Mob(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		factor =  2/3.0
		self.image = pg.transform.scale(game.mob_img, (int(factor*180), int(factor*130)))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 50*factor
		#pg.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.spawn()

	def update(self):
		self.rect.x += self.speedx
		if self.rect.x > WIDTH:
			self.spawn()		

	def spawn(self):
		self.rect.x,self.rect.y = (randrange(-200, -100),randrange(0,4*HEIGHT/7) )
		self.speedx = randrange(2,MOB_SPEED)

class Arrow(pg.sprite.Sprite):
	def __init__(self, player, game, vec_butt, vec_tip, rot):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.transform.scale(self.game.arrow_img,(40,40))#self.game.arrow_img
		self.image_orig = self.image
		#self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20 * 80/128
		self.pos = vec(player.rect.center)+vec(5,-5)
		vec_i = vec_butt + self.pos
		self.vec_butt = vec_butt
		self.vec_tip = vec_tip
		self.rect.bottom = vec_i.y
		self.rect.centerx = vec_i.x 
		self.acc = vec(0, GRAVITY)
		d = (vec_tip - vec_butt) 
		#self.vel = d * ARROW_SPEED/ sqrt(d.x*d.x + d.y*d.y)
		self.theta = radians(rot+ARROW_ANGLE)
		self.vel = vec(0,0)#vec(cos(theta), -sin(theta)) * ARROW_SPEED
		self.rot = rot 
		self.prev_vec = vec(0,0)

	
	def rotate(self, angle):
		self.rot = angle 
		new_image = pg.transform.rotate(self.image_orig, self.rot)
		old_pivot = self.rect.center
		self.image = new_image
		self.rect = self.image.get_rect()
		self.rect.center = old_pivot
		pg.draw.circle(self.image_orig, RED, self.rect.center, self.radius)
		
	def update(self):
		"""self.rotate(self.rot + atan(self.vel.y/self.vel.x) -13 )
		self.vel += self.acc 
		self.pos += self.vel + 0.5 * self.acc"""

		self.pos += self.vel
		#self.rotate(atan((self.prev_vec.y - self.pos.y)/(self.prev_vec.x - self.pos.x)) )

		self.prev_vec = self.pos
		#self.pos += self.vel
		self.rect.center = self.pos

		'''