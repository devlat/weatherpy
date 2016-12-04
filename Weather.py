#! -*- coding: utf-8 -*-
import urllib2, json, datetime, sys, smtplib;
from email.mime.text import MIMEText

class Weather:
    def __init__(self):
        try:
            configJsonFile = open('./config/main.json', 'r');
        except IOError:
            print "IOError";
            sys.exit();
        self.config = json.loads(configJsonFile.read());
        configJsonFile.close();

    def getData(self):
        apiConfig = self.config['api'];

        url = apiConfig['url'] + '?' + 'id=%s&APPID=%s&units=metric' % (apiConfig['city_id'], apiConfig['key']);

        urlObj = urllib2.urlopen(url);

        weatherData = json.loads(urlObj.read());

        currentTime = datetime.datetime.now().strftime('%d.%m.%Y[%H-%M-%S]');

        output = open('./result/{0}_{1}.txt'.format(weatherData['name'], currentTime), 'w');
        output.write('Datetime: %s\n' % currentTime);
        output.write('City: %s\n' % weatherData['name']);
        output.write('Temp: %d\n' % weatherData['main']['temp']);
        output.write('Weather: %s\n' % weatherData['weather'][0]['main']);
        output.write('Wind speed: %d\n' %  weatherData['wind']['speed']);
        try:
            self.sendData();
        except:
            pass;
        output.close();

    def sendData(self):
        # Для работы нужен установленный Postfix(или любой другой сервер)
        msg = MIMEText("Testing e-mail");
        msg['Subject'] = 'TEST EMAIL';
        msg['From'] = 'local@local.com';
        msg['To'] = 'mgtttt@mail.ru';

        s = smtplib.SMTP('localhost');
        s.sendmail('local@local.com', ['mgtttt@mail.ru'], msg.as_string());
        s.quit();
