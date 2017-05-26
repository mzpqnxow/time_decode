#!/usr/bin/env python
from dateutil import parser as duparser
import datetime
import logging
import struct
from binascii import hexlify, unhexlify
import argparse
import sys

__author__='Corey Forman'
__date__='25 May 17'
__version__='0.07'
__description__='Python CLI Date Time Conversion Tool'

class DateDecoder(object):
  def __init__(self):
    self.processed_unix_seconds = None
    self.processed_unix_milli = None
    self.processed_windows_filetime_64 = None
    self.processed_windows_little_endian_64 = None
    self.processed_chrome_time = None
    self.processed_active_directory_time = None
    self.processed_unix_hex_32 = None
    self.processed_unix_hex_32le = None
    self.processed_cookie = None
    self.processed_ole_be = None
    self.processed_ole_le = None
    self.epoch_1601 = 11644473600000000
    self.epoch_1970 = datetime.datetime(1970,1,1)
    self.hundreds_nano = 10000000
    self.epoch_as_filetime = 116444736000000000
    self.epoch_1899 = datetime.datetime(1899,12,30,0,0,0)

  def run(self):
    if len(sys.argv[1:])==0:
      argparse.print_help()
      argparse.exit()
    logging.info('Launching Date Decode')
    logging.info('Processing Timestamp: ' + sys.argv[2])
    logging.info('Input Time Format: ' + sys.argv[1])
    logging.info('Starting Date Decoder v.' +str(__version__))
    if args.unix:
      try:
        self.convertUnixSeconds()
        print "Unix Seconds: " + self.processed_unix_seconds
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.umil:
      try:
        self.convertUnixMilli()
        print "Unix Milliseconds: " + self.processed_unix_milli
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.ft:
      try:
        self.convertWindowsFiletime_64()
	print "Windows Filetime 64 Bit: " + self.processed_windows_filetime_64
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.fle:
      try:
	self.convertWindowsLittleEndian_64()
        print "Windows Filetime 64 Little Endian: " + self.processed_windows_little_endian_64
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))   
    elif args.goog:
      try:
	self.convertChromeTimestamps()      
	print "Google Chrome Time: " + self.processed_chrome_time
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.active:
      try:
	self.convertActiveDirectory_DateTime()
	print "Active Directory Timestamp: " + self.processed_active_directory_time
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.uhbe:
      try: 
	self.convertUnixHex32BE()
	print "Unix Hex 32 Bit Big Endian: " + self.processed_unix_hex_32
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.uhle:
      try:
        self.convertUnixHex32LE()
	print "Unix Hex 32 Bit Little Endian: " + self.processed_unix_hex_32le
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.guess:
      try:
        self.convertAll()
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.cookie:
      try:
        self.convertCookieDate()
	print "Windows Cookie Date: " + self.processed_cookie
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.oleb:
      try:
	self.convertOleBE()
        print "Windows OLE 64 bit double Big Endian: " + self.processed_ole_be
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))
    elif args.olel:
      try:
        self.convertOleLE()
        print "Windows OLE 64 bit double Little Endian: " + self.processed_ole_le
      except Exception, e:
        logging.error(str(type(e)) + "," + str(e))

  def convertAll(self):
    
    self.processed_unix_seconds = 'N/A'
    self.processed_unix_milli = 'N/A'
    self.processed_windows_little_endian_64 = 'N/A'
    self.processed_windows_filetime_64 = 'N/A'
    self.processed_chrome_time = 'N/A'
    self.processed_active_directory_time = 'N/A'
    self.processed_unix_hex_32 = 'N/A'
    self.processed_unix_hex_32le = 'N/A'
    self.processed_cookie = 'N/A'
    self.processed_ole_be = 'N/A'
    self.processed_ole_le = 'N/A'

    print '\nGuessing Timestamp Format\n'

    self.convertUnixSeconds()
    self.convertUnixMilli()
    self.convertWindowsLittleEndian_64()
    self.convertWindowsFiletime_64()
    self.convertChromeTimestamps()
    self.convertActiveDirectory_DateTime()
    self.convertUnixHex32BE()
    self.convertUnixHex32LE()
    self.convertCookieDate()
    self.convertOleBE()
    self.convertOleLE()
    self.output()
    print '\r' 

  def convertUnixSeconds(self):
    try:
      self.processed_unix_seconds = datetime.datetime.utcfromtimestamp(float(sys.argv[2])).strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_unix_seconds = 'N/A' #str(type(e).__name__)

  def convertUnixMilli(self):
    try:
      self.processed_unix_milli = datetime.datetime.utcfromtimestamp(float(sys.argv[2]) / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_unix_milli = 'N/A'

#    elif args.unix == 'formatted':
#      try:
#        converted_time = duparser.parse(args.unix)
#        self.processed_unix_seconds = str((converted_time - self.epoch_1970).total_seconds())
#      except Exception, e:
#        logging.error(str(type(e)) + "," + str(e))
#        self.processed_unix_seconds = str(type(e).__name__)

  def convertWindowsFiletime_64(self):
    try:
      base10_microseconds = int(sys.argv[2], 16) / 10
      datetime_obj = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=base10_microseconds)
      self.processed_windows_filetime_64 = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_windows_filetime_64 = 'N/A' #str(type(e).__name__)

#    elif args.ft == 'formatted':
#      try:
#        converted_time = duparser.parse(args.ft)
#        minus_epoch = converted_time - datetime.datetime(1601,1,1)
#        calculated_time = minus_epoch.microseconds + (minus_epoch.seconds * 1000000) + (minus_epoch.days * 86400000000)
#        self.processed_windows_filetime_64 = str(hex(int(calculated_time)*10))
#        print self.processed_windows_filetime_64
#      except Exception, e:
#        logging.error(str(type(e)) + "," + str(e))
#        self.processed_windows_filetime_64 = str(type(e).__name__)

  def convertWindowsLittleEndian_64(self):
    try:
      converted_time = struct.unpack("<Q", unhexlify(sys.argv[2]))[0]
      datetime_obj = datetime.datetime(1601,1,1,0,0,0) + datetime.timedelta(microseconds=converted_time /10)
      self.processed_windows_little_endian_64 = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_windows_little_endian_64 = 'N/A' #str(type(e).__name__)

#    elif args.fle == 'formatted':
#      try:
#        converted_time = duparser.parse(args.fle)
#        minus_epoch = converted_time - datetime.datetime(1601,1,1,0,0,0)
#        calculated_time = minus_epoch.microseconds + (minus_epoch.seconds * 1000000) + (minus_epoch.days * 86400000000)
#        self.processed_windows_little_endian_64 = str(hexlify(struct.pack("<Q",int(calculated_time*10))))
#      except Exception, e:
#        logging.error(str(type(e)) + "," + str(e))
#        self.processed_windows_little_endian_64 = str(type(e).__name__)


  def convertChromeTimestamps(self):
    try:
      converted_time = datetime.datetime.utcfromtimestamp((float(sys.argv[2])-self.epoch_1601)/1000000)
      self.processed_chrome_time = converted_time.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_chrome_time = 'N/A' #str(type(e).__name__)

#    elif args.goog == 'formatted':
#      try:
#        converted_time = duparser.parse(args.goog)
#        chrome_time = (converted_time - self.epoch_1970).total_seconds()*1000000 + self.epoch_1601
#        self.processed_chrome_time = str(int(chrome_time))
#	print self.processed_chrome_time
#      except Exception, e:
#        logging.error(str(type(e)) + "," + str(e))
#        self.processed_chrome_time = str(type(e).__name__)

  def convertActiveDirectory_DateTime(self):
    try:
      part2, part1 = [int(h, base=16) for h in sys.argv[2].split(':')]
      converted_time = struct.unpack('>Q', struct.pack('>LL', part1, part2))[0]
      datetime_obj = datetime.datetime.utcfromtimestamp((converted_time - self.epoch_as_filetime) / self.hundreds_nano)
      self.processed_active_directory_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_active_directory_time = 'N/A' #str(type(e).__name__)

#    elif args.active == 'formatted':
#      try:
#        converted_time = duparser.parse(args.active)
#        minus_epoch = converted_time - datetime.datetime(1601,1,1,0,0,0)
#        calculated_time = minus_epoch.microseconds + (minus_epoch.seconds * 1000000) + (minus_epoch.days * 86400000000)
#        self.processed_active_directory_time = str(hexlify(struct.pack("<Q",int(calculated_time*10))))
#	print self.processed_active_directory_time
#      except Exception, e:
#        logging.error(str(type(e)) + "," + str(e))
#        self.processed_windows_little_endian_64 = str(type(e).__name__)

  def convertUnixHex32BE(self):
    try:
      to_dec = int(sys.argv[2], 16)
      self.processed_unix_hex_32 = datetime.datetime.utcfromtimestamp(float(to_dec)).strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_unix_hex_32 = 'N/A' #str(type(e).__name__)

#   elif args.uhbe == 'formatted':
#     try:
#       converted_time = duparser.parse(args.uhbe)
#       self.processed_unix_hex_32 = str((converted_time - self.epoch_1970).total_seconds())
#     except Exception, e:
#       logging.error(str(type(e)) + "," + str(e))
#       self.processed_unix_hex_32 = str(type(e).__name__)

  def convertUnixHex32LE(self):
    try:
      to_dec = struct.unpack("<L", unhexlify(sys.argv[2]))[0]
      self.processed_unix_hex_32le = datetime.datetime.utcfromtimestamp(float(to_dec)).strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_unix_hex_32le = 'N/A' #str(type(e).__name__)

  def convertCookieDate(self):
    try:
      low, high = [int(h, base=10) for h in sys.argv[2].split(',')]
      calc = 10**-7 * (high * 2**32 + low) - 11644473600
      datetime_obj = datetime.datetime.utcfromtimestamp(calc)
      self.processed_cookie = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_cookie = 'N/A'

  def convertOleBE(self):
    try:
      delta = struct.unpack('>d',struct.pack('>Q', int(sys.argv[2], 16)))[0]
      datetime_obj = self.epoch_1899 + datetime.timedelta(days=delta)
      self.processed_ole_be = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_ole_be = 'N/A'

  def convertOleLE(self):
    try:
      from_be = sys.argv[2].decode('hex')
      to_le = from_be[::-1].encode('hex')
      delta = struct.unpack('>d',struct.pack('>Q', int(to_le, 16)))[0]
      datetime_obj = self.epoch_1899 + datetime.timedelta(days=delta)
      self.processed_ole_le = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    except Exception, e:
      logging.error(str(type(e)) + "," + str(e))
      self.processed_ole_le = 'N/A'

  def output(self):
    if isinstance(self.processed_unix_seconds, str):
      print "Unix Seconds: "  + self.processed_unix_seconds

    if isinstance(self.processed_unix_milli, str):
      print "Unix Milliseconds: " + self.processed_unix_milli

    if isinstance(self.processed_windows_little_endian_64, str):
      print "Windows FILETIME 64 LE: " + self.processed_windows_little_endian_64
 
    if isinstance(self.processed_windows_filetime_64, str):
      print "Windows FILETIME 64: " + self.processed_windows_filetime_64

    if isinstance(self.processed_chrome_time, str):
      print "Google Chrome: " + self.processed_chrome_time

    if isinstance(self.processed_active_directory_time, str):
      print "Active Directory DateTime: " + self.processed_active_directory_time

    if isinstance(self.processed_unix_hex_32, str):
      print "Unix Hex 32 Bit BE: " + self.processed_unix_hex_32 

    if isinstance(self.processed_unix_hex_32le, str):
      print "Unix Hex 32 Bit LE: " + self.processed_unix_hex_32le

    if isinstance(self.processed_cookie, str):
      print "Windows Cookie Date: " + self.processed_cookie

    if isinstance(self.processed_ole_be, str):
      print "Windows OLE 64 Bit double Big Endian: " + self.processed_ole_be

    if isinstance(self.processed_ole_le, str):
      print "Windows OLE 64 Bit double Little Endian: " + self.processed_ole_le

if __name__ == '__main__':
  argparse = argparse.ArgumentParser(description="Date Decode Time Converter")
  argparse.add_argument('--unix', metavar='<value>', help='convert from Unix Seconds', required=False)
  argparse.add_argument('--umil', metavar='<value>', help='convert from Unix Milliseconds', required=False)
  argparse.add_argument('--ft', metavar='<value>', help='convert from Windows FILETIME 64', required=False)
  argparse.add_argument('--fle', metavar='<value>', help='convert from Windows FILETIME 64 Little Endian', required=False)
  argparse.add_argument('--goog', metavar='<value>', help='convert from Google Chrome time', required=False)
  argparse.add_argument('--active', metavar='<value>', help='convert from Active Directory DateTime', required=False)
  argparse.add_argument('--uhbe', metavar='<value>', help='convert from Unix Hex 32 Bit Big Endian', required=False)
  argparse.add_argument('--uhle', metavar='<value>', help='convert from Unix Hex 32 Bit Little Endian', required=False)
  argparse.add_argument('--cookie', metavar='<value>', help='convert from Windows Cookie Date (Low Value, High Value)', required=False)
  argparse.add_argument('--oleb', metavar='<value>', help='convert from Windows OLE 64 bit Big Endian - remove 0x and spaces!\n Example from SRUM: 0x40e33f5d 0x97dfe8fb should be 40e33f5d97dfe8fb', required=False)
  argparse.add_argument('--olel', metavar='<value>', help='convert from Windows OLE 64 bit Little Endian', required=False)
  argparse.add_argument('--guess', metavar='<value>', help='guess format and output possibilities', required=False)
  argparse.add_argument('--version', '-v', action='version', version='%(prog)s' +str( __version__))
  args = argparse.parse_args()

  log_path = 'decoder.log'
  logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(funcName)s | %(message)s', filemode='a')
  logging.debug('System ' + sys.platform)
  logging.debug('Version ' + sys.version)
  dd = DateDecoder()
  dd.run()
