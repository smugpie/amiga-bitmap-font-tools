# encoding: utf-8

###########################################################################################################
#
#
#	File Format Plugin
#	Implementation for exporting fonts through the Export dialog
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/File%20Format
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
import json
from GlyphsApp import *
from GlyphsApp.plugins import *
from metrics import getHeight, getDepth
from drawing import drawPixel
from style import getHumanReadableStyle

class OpenAmigaJsonFont(FileFormatPlugin):
	@objc.python_method
	def settings(self):
		self.name = "Amiga Bitmap Font"
		self.icon = 'ExportIcon'
		self.toolbarPosition = 100
	
	@objc.python_method
	def read(self, filepath, fileType):
		font = GSFont()
		font.disableUpdateInterface()
		try:
			with open(filepath, encoding='utf-8') as binaryFile:
				amigaFont = json.load(binaryFile)

				glyphsFont = GSFont()
				glyphsFont.familyName = amigaFont['name']
				glyphsFont.upm = 1000
				glyphsFont.descriptions['ENG'] = 'Converted by amiga-bitmap-font-tools'

				glyphsFont.disableUpdateInterface()

				master = glyphsFont.masters[0]
				master.name = getHumanReadableStyle(amigaFont['style'])

				fontSize = amigaFont['ySize']
				baseline = amigaFont['baseline']
				pixelSize = int(glyphsFont.upm / fontSize)
				pixelsBelowBaseline = fontSize - baseline

				# work out x-height from the letter x (ASCII code 120)
				xHeight = getHeight(
					amigaFont['glyphs']['120']['bitmap'],
					pixelsBelowBaseline
				)
				if xHeight > 0:
					master.xHeight = xHeight * pixelSize

				# work out cap height from the letter E (ASCII code 69)
				capHeight = getHeight(
					amigaFont['glyphs']['69']['bitmap'],
					pixelsBelowBaseline
				)
				if capHeight > 0:
					master.capHeight = capHeight * pixelSize

				# work out ascender from the letter b (ASCII code 98)
				ascender = getHeight(
					amigaFont['glyphs']['98']['bitmap'],
					pixelsBelowBaseline
				)
				if ascender > 0:
					master.ascender = ascender * pixelSize

				# work out descender from the letter p (ASCII code 112)
				descender = getDepth(
					amigaFont['glyphs']['112']['bitmap'],
					pixelsBelowBaseline
				)
				if descender < 0:
					master.descender = descender * pixelSize

				for char, amigaGlyph in amigaFont['glyphs'].items():
					glyph = GSGlyph(amigaGlyph['character'])
					glyphsFont.glyphs.append(glyph)
					layer = glyph.layers[0]
					
					layer.width = ((amigaGlyph['spacing'] + amigaGlyph['kerning']) * pixelSize) if amigaFont['flags']['proportional'] else (amigaFont['xSize'] * pixelSize)

					for rowNumber, rowData in enumerate(amigaGlyph['bitmap']):
						rowPosition = fontSize - rowNumber - pixelsBelowBaseline
						for colNumber, colData in enumerate(rowData):
							colPosition = (colNumber + amigaGlyph['kerning']) if amigaFont['flags']['proportional'] else colNumber
							if colData == '1':
								rect = drawPixel( rowPosition, colPosition, pixelSize )
								layer.shapes.append(rect)
						layer.removeOverlap()
		except:
			print(traceback.format_exc())
		font.enableUpdateInterface()
		return glyphsFont

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
