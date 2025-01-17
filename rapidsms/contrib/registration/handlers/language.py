#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsms.conf import settings
from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler


class LanguageHandler(KeywordHandler):
    """
    Allow remote users to set their preferred language, by updating the
    ``language`` field of the Contact associated with their connection.
    """

    keyword = "language|lang"

    def help(self):
        self.respond("To set your language, send LANGUAGE <CODE>")

    def handle(self, text):
        if self.msg.connections[0].contact is None:
            return self.respond_error(
                "You must JOIN or REGISTER yourself before you can " +
                "set your language preference.")

        t = text.lower()
        for code, name in settings.LANGUAGES:
            if t != code.lower() and t != name.lower():
                continue

            self.msg.connections[0].contact.language = code
            self.msg.connections[0].contact.save()

            return self.respond(
                "I will speak to you in %(language)s." % {
                    'language': name})

        return self.respond_error(
            'Sorry, I don\'t speak "%(language)s".' % {
                'language': text})
