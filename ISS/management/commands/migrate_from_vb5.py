import random

import mysql.connector

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from ISS.models import *

class Command(BaseCommand):
    help = 'Migrates a vBulletin 5 database to ISS'

    db_user = 'root'
    db_pass = ''
    db_name = 'vB'
    db_host = 'localhost'
    category_pks = []

    def add_arguments(self, parser):
        # parser.add_argument('n', type=int)
        pass

    def mig_users(self, cnx, cursor):
        query = 'SELECT * FROM user;'
        cursor.execute(query)

        o2n_map = {}
        for user in cursor:
            new_user = Poster(username=user['username'],
                              email=user['email'])
            try:
                new_user.save()
                o2n_map[user['userid']] = new_user
            except IntegrityError:
                print 'Duplicate, could not save user: %s' % user['username']
                o2n_map[user['userid']] = Poster.objects.get(
                    username=user['username'])

        return o2n_map

    def mig_forums(self, cnx, cursor):
        query = """
            SELECT forum.* FROM node AS forum
                JOIN node AS forum_group
                    ON forum.parentid = forum_group.nodeid
                JOIN node AS forum_parent
                    ON forum_group.parentid = forum_parent.nodeid
                WHERE
                    forum_parent.urlident = 'forum'
        """

        cursor.execute(query)
        o2n_map = {}
        for forum in cursor:
            new_forum = Forum(
                name=forum['title'],
                description=forum['description'],
                priority=forum['displayorder'])

            new_forum.save()

            o2n_map[forum['nodeid']] = new_forum.pk

        return o2n_map


    def handle(self, *args, **kwargs):

        cnx = mysql.connector.connect(user=self.db_user,
                                      password=self.db_pass,
                                      host=self.db_host,
                                      database=self.db_name)
        cursor = cnx.cursor(dictionary=True)

        #user_pk_map = self.mig_users(cnx, cursor)
        self.mig_forums(cnx, cursor)
        
        cnx.close()

        
