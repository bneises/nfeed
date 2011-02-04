#!/bin/sh
URLShttp='http://spreadsheets.google.com/pub?key=tdCO0yKGjD7kbYSsixw0JBA&single=true&gid=0&output=txt'
TERMShttp='http://spreadsheets.google.com/pub?key=tiRxbzQhg7_vw1BBElMXEPg&single=true&gid=0&output=txt'

python nfeed-redis.py -u $URLShttp -t $TERMShttp
