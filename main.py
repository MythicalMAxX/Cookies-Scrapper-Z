from requests import get
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import csv

Domains = {"Akamai":"https://www.akamai.com/",
        "Kissmetrics analytics service":"https://www.kissmetrics.io/",
        "Google Analytics service":"https://www.google.com/",
        "Google Website Optimizer":"https://www.google.com/",
        "Google Universal Analytics":"https://www.google.com/",
        "CloudFlare":"https://www.cloudflare.com/",
        "OneTrust":"https://www.onetrust.com/",
        "Quantcast":"https://www.quantcast.com/"}

def get_hostname(description):
    service_providers = ["Quantcast", "Google Analytics service", "Google Website Optimizer",
                         "Google Universal Analytics",
                         "Akamai", "Kissmetrics analytics service", "Mint Analytics software", "CloudFlare", "OneTrust"]
    if description != "":
        for element in service_providers:
            if element in description:
                host = element
                break
    elif description == "":
        host = "Data Not Available"

    try:
        return host
    except:
        return "Unknown"

def get_description(cookie_urls):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    description_data = get(cookie_urls, headers=header).text
    p = BeautifulSoup(description_data, 'html.parser')
    descript = p.find_all("div", {"class": "full-width"})
    descript = str(descript)
    p1 = BeautifulSoup(descript, 'lxml')
    desc = p1.find_all("p")
    desc = re.sub('<[^<]+?>', '', str(desc))
    desc = re.sub(r",\sThe\smain\spurpose.*$", "", str(desc))
    desc = desc.replace("\n","")
    try:
        desc = desc[4:]
    except:
        desc = "No Resources Found"

    if desc == "":
        desc = "No Resources Found"
    return desc

raw_output = []
existing_cookies = []
def create_entry(dict, url):
    if dict["Cookiename"] in existing_cookies:
        return 0
    cookie_url = "https://cookiepedia.co.uk/cookies/" + dict["Cookiename"]
    dict["Cookie URL"] = cookie_url
    dict["URL"] = url
    if dict["Purpose"]=="Targeting/AdvertisingCookie name":
        dict["Purpose"] = "Targeting/Advertising"
    about_cookies = get_description(cookie_url)
    host_name = get_hostname(about_cookies)

    try:
        domain_name = Domains[host_name]
    except:
        domain_name = "Unknown"

    writer.writerow([url, dict["Cookiename"],domain_name,host_name, dict["Purpose"], about_cookies, cookie_url,dict["Is Secure"],dict["Is HTTP Only"],dict["Path"]])
    existing_cookies.append(dict["Cookiename"])

    My_dictionary = {"Url":url,"Cookie Name":dict["Cookiename"],"Domain":domain_name,"Host Name":host_name,"Purpose":dict["Purpose"],"Description":about_cookies,"Cookie URL": cookie_url,"Is Secure":dict["Is Secure"],"Is HTTP Only":dict["Is HTTP Only"],"Path":dict["Path"]}
    raw_output.append((My_dictionary))

def req(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    with get(url, headers=header) as response:
        pass
    print(response)
    print(response.text)
    parser = BeautifulSoup(response.text, 'html.parser')
    div = parser.find_all("div", {"class": "accordion-content"})
    div = re.sub('<[^<]+?>', '', str(div))
    div = div.replace(" ", "")
    div = div.replace("\r", "")
    div = div.replace("\n", "")
    div = div.replace("[", "")
    div = div.replace("]", "")
    div = div.replace("AdvertisingCookiename", "AdvertisingMoreCookiename")
    div = div.replace("UnknownCookiename", "UnknownMoreCookiename")
    div = div.replace("Advertising,Cookiename", "AdvertisingMoreCookiename")
    div = div.replace("Unknown,Cookiename", "UnknownMoreCookiename")

    list1 = div.split("More")
    data = []
    for strings in list1:
        string = re.sub(r"AboutthisCookie.*$", "", str(strings))
        string = string.replace("/Purpose:", "/ ||Purpose:")
        string = string.replace("?", ":")
        string = string.replace("Is", "||Is")
        string = string.replace("Path", "||Path")
        string = string.replace("||", ",")
        string = string.replace("IsSecure:", "Is Secure,")
        string = string.replace("IsHTTPOnly:", "Is HTTP Only,")
        string = string.replace("Path:", "Path,")
        string = string.replace("Purpose:", "Purpose,")
        string = string.replace("Cookiename:", "Cookiename,")

        data.append(string)
    data = list(OrderedDict.fromkeys(data))
    if data[len(data)-1] == "":
        data.pop()
    return data

links = ['d1447tq2m68ekg.cloudfront.net', 'd191y0yd6d0jy4.cloudfront.net', 'd1l6p2sc9645hc.cloudfront.net', 'd1q62gfb8siqnm.cloudfront.net', 'd1z2jf7jlzjs58.cloudfront.net', 'd22xmn10vbouk4.cloudfront.net', 'd24n15hnbwhuhn.cloudfront.net', 'd26b395fwzu5fz.cloudfront.net', 'd26opx5dl8t69i.cloudfront.net', 'd2blwevgjs7yom.cloudfront.net', 'd2eeipcrcdle6.cloudfront.net', 'd2gfdmu30u15x7.cloudfront.net', 'd2hkbi3gan6yg6.cloudfront.net', 'd2oh4tlt9mrke9.cloudfront.net', 'd2r1yp2w7bby2u.cloudfront.net', 'd2vig74li2resi.cloudfront.net', 'd2zah9y47r7bi2.cloudfront.net', 'd31j93rd8oukbv.cloudfront.net', 'd31qbv1cthcecs.cloudfront.net', 'd32hwlnfiv2gyn.cloudfront.net', 'd38nbbai6u794i.cloudfront.net', 'd3hmp0045zy3cs.cloudfront.net', 'd3vbj265bmdenw.cloudfront.net', 'd6tizftlrpuof.cloudfront.net', 'd8rk54i4mohrb.cloudfront.net', 'd9jmv9u00p0mv.cloudfront.net', 'dd6zx4ibq538k.cloudfront.net', 'decibelinsight.net', 'demandjump.com', 'devatics.io', 'digitalscirocco.net', 'digitru.st', 'dkpklk99llpj0.cloudfront.net', 'dn3y71tq7jf07.cloudfront.net', 'dnn506yrbagrg.cloudfront.net', 'dotmailer-surveys.com', 'dsp.io', 'dsply.com', 'dsyszv14g9ymi.cloudfront.net', 'dynapis.info', 'easypolls.net', 'ebiquitymedia.com', 'econda-monitor.de', 'efm.me', 'egain.com', 'ekmpinpoint.co.uk', 'ekomi.de', 'elitechnology.com', 'enfusen.com', 'epoq.de', 'esearchvision.com', 'ethn.io', 'etracker.de', 'evgnet.com', 'evidon.com', 'evisitanalyst.com', 'exponea.com', 'extreme-dm.com', 'ezoic.net', 'fastclick.net', 'fastly-insights.com', 'feedbackify.com', 'feedmagnet.com', 'feefo.com', 'fits.me', 'fivetran.com', 'flixfacts.co.uk', 'foreseeresults.com', 'fospha.com', 'fullstory.com', 'gaug.es', 'geni.us', 'getclicky.com', 'getscenario.com', 'gexperiments1.com', 'gigya.com', 'glimr.io', 'globalwebindex.net', 'google-analytics.com', 'govmetric.com', 'granify.com', 'grvcdn.com', 'heapanalytics.com', 'heatmap.it', 'hexagon-analytics.com', 'histats.com', 'hits.io', 'hitslink.com', 'hitsprocessor.com', 'hmcdn.baidu.com', 'hootsuite.com', 'hotjar.com', 'hotjar.io', 'hotukdeals.com', 'hupso.com', 'ibmcloud.com', 'igodigital.com', 'iljmp.com', 'imrg.org', 'imrworldwide.com', 'infinity-tracking.net', 'innomdc.com', 'insightexpressai.com', 'inspectlet.com', 'intenthq.com', 'interstateanalytics.com', 'ioam.de', 'ipv6test.net', 'iteratehq.com', 'js-cdn.dynatrace.com', 'jsonip.com', 'kaizenplatform.net', 'kameleoon.com', 'kampyle.com', 'keyade.com', 'keynote.com', 'korrelate.net', 'krxd.net', 'lightstep.com', 'linkcious.com', 'litix.io', 'lockerdome.com', 'lognormal.net', 'logo-net.co.uk', 'loop11.com', 'lp4.io', 'luckyorange.net', 'lumatag.co.uk', 'lypn.net', 'm-decision.com', 'marchex.io', 'marketizator.com', 'marketo.net', 'matheranalytics.com', 'matomo.cloud', 'maxymiser.net', 'meclabsdata.com', 'mediahawk.co.uk', 'mediaiqdigital.com', 'medio.com', 'miaozhen.com', 'micpn.com', 'monetate.net', 'mopinion.com', 'mouse3k.com', 'mouseflow.com', 'mousestats.com', 'mpstat.us', 'mxpnl.com', 'mybuys.com', 'myvisualiq.net', 'naytev.com', 'nccgroup-webperf.com', 'needle.com', 'nosto.com', 'nowinteract.com', 'nt.vc', 'ntoklo.com', 'ntv.io', 'okta.com', 'ometria.com', 'omtrdc.net', 'oneall.com', 'ontame.io', 'ophan.co.uk', 'opinionbar.com', 'opinionstage.com', 'optilead.co.uk', 'optimizely.com', 'optimove.net', 'otracking.com', 'pagesense.io', 'peerius.com', 'peermapcontent.affino.com', 'pendo.io', 'persuasionapi.com', 'petametrics.com', 'picreel.com', 'pictela.net', 'pingdom.net', 'placed.com', 'planning-inc.co.uk', 'polldaddy.com', 'powerreviews.com', 'pswec.com', 'pulseinsights.com', 'qeryz.com', 'qmerce.com', 'qmodal.azurewebsites.net', 'qualaroo.com', 'qualtrics.com', 'quantummetric.com', 'qubitproducts.com', 'questionpro.com', 'qzzr.com', 'raac33.net', 'rampanel.com', 'reactful.com', 'realytics.net', 'recobell.io', 'recommend.pro', 'reevoo.com', 'res-x.com', 'research-int.se', 'researchnow.com', 'reson8.com', 'responsetap.com', 'reviews.co.uk', 'reviews.io', 'revolvermaps.com', 'richrelevance.com', 'rlcdn.com', 'rovicorp.com', 'rubikloud.com', 'ruleranalytics.com', 'rummblelabs.com', 'sail-track.com', 'salesloft.com', 'samplicio.us', 'sc-static.net', 'scarabresearch.com', 'searchanise.com', 'securestudies.com', 'segment.io', 'segmentstream.com', 'segmint.net', 'sellpoints.com', 'semasio.net', 'servicetick.com', 'servmetric.com', 'sesamestats.com', 'sidereel.com', 'site24x7rum.com', 'sitemeter.com', 'skyglue.com', 'smarterremarketer.net', 'smartlook.com', 'sodahead.com', 'sophus3.com', 'speedcurve.com', 'spiceworks.com', 'stamped.io', 'statcounter.com', 'statful.com', 'stats.wp.com', 'stellaservice.com', 'stormiq.com', 'sub2tech.com', 'survata.com', 'surveygizmo.eu', 'surveymonkey.com', 'survicate.com', 'tag4arm.com', 'tctm.co', 'tellaparts.com', 'thefilter.com', 'themessagecloud.com', 'tmvtp.com', 'tns-counter.ru', 'trackalyzer.com', 'trackedweb.net', 'treasuredata.com', 'trialfire.com', 'trovus.co.uk', 'truconversion.com', 'truedash.com', 'truefitcorp.com', 'trustpilot.com', 'tryzens-analytics.com', 'tweetmeme.com', 'u5e.com', 'umbel.com', 'upsellit.com', 'usabilitytools.com', 'useitbetter.com', 'userneeds.dk', 'userreplay.net', 'userreport.com', 'userzoom.com', 'v12group.com', 'veruta.com', 'vidpulse.com', 'vimeo.com', 'visualwebsiteoptimizer.com', 'vizu.com', 'vizzit.se', 'voicefive.com', 'vouchedfor.co.uk', 'vwo.com', 'wayfair.com', 'wcfbc.net', 'wdfl.co', 'web-call-analytics.com', 'webabacus.com', 'webdissector.com', 'webforensics.co.uk', 'websta.me', 'webtuna.com', 'wishabi.net', 'woopra.com', 'wowanalytics.co.uk', 'wt-eu02.net', 'wurfl.io', 'www.sc.pagesA.net', 'wzrkt.com', 'xclusive.ly', 'xsellapp.com', 'y-track.com', 'yadro.ru', 'zafu.com', 'zarget.com', 'zn3vgszfh.fastestcdn.net', 'zoover.co.uk', 'zqtk.net', '176.74.183.134', '1xrun.com', '4finance.com', 'ably.io', 'acsbap.com', 'acsbapp.com', 'addevent.com', 'addtocalendar.com', 'adledge.com', 'adrta.com', 'advolution.de', 'adyen.com', 'affirm.com', 'aheadworks.com', 'ajax.cloudflare.com', 'algolia.io', 'alphassl.com', 'animatedjs.com', 'apligraf.com.br', 'appelsiini.net', 'arcgisonline.com', 'areyouahuman.com', 'aspnetcdn.com', 'auth0.com', 'authorize.net', 'avcosystems.com', 'avg.com', 'bankrate.com', 'barclaycardsmartpay.com', 'bit.ly', 'boldapps.net', 'bolt.com', 'bootcss.com', 'bootstrapcdn.com', 'bpay.co.uk', 'braintreegateway.com', 'bugherd.com', 'cachefly.net', 'cafonline.org', 'cast.rocks', 'cdn-net.com', 'cdn.jsdelivr.net', 'cdn.mouseflow.com', 'cdn.shopify.com', 'cdn2.editmysite.com', 'cdn77.org', 'cdnjs.cloudflare.com', 'certum.pl', 'checkrate.co.uk', 'checkout.com', 'cloudfront.net', 'cludo.com', 'cnstrc.com', 'coherentpath.com', 'colbenson.com', 'comodo.net', 'comodoca4.com', 'contentful.com', 'cookie-script.com', 'cookiebot.com', 'cookieq.com', 'cookiereports.com', 'crcom.co.uk', 'createjs.com', 'csi.gstatic.com', 'd1azc1qln24ryf.cloudfront.net', 'd2wy8f7a9ursnm.cloudfront.net', 'd37gvrvc0wt4s1.cloudfront.net', 'd3c3cq33003psk.cloudfront.net', 'd3tjaysgumg9lf.cloudfront.net', 'digicert.com', 'divido.com', 'dmca.com', 'dpstatic.com', 'dropboxusercontent.com', 'dummyimage.com', 'dwcdn.net', 'dynamicconverter.com', 'edaa.eu', 'edgecastdns.net', 'edgefonts.net', 'elevaate.technology', 'elicitapp.com', 'empathybroker.com', 'ensighten.com', 'entrust.net', 'equiniti.com', 'errorception.com', 'euroland.com', 'everesttech.net', 'eway.com.au', 'experianmarketingservices.digital', 'fastly.net', 'fiftyone.com', 'firepush.io', 'firestore.googleapis.com', 'flaticons.net', 'flexshopper.com', 'fontawesome.com', 'fontdeck.com', 'fonts.gstatic.com', 'fonts.net', 'footprint.net', 'fortawesome.com', 'forter.com', 'foxentry.cz', 'foxycart.com', 'fqtag.com', 'freegeoip.net', 'freshchat.com', 'freshworksapi.com', 'gccdn.net', 'geoplugin.net', 'georeferencer.com', 'geotrust.com', 'getsitecontrol.com', 'gfycat.com', 'globalsign.net', 'goadservices.com', 'gointerpay.net', 'gomoxie.solutions', 'googleapis.com', 'googlecommerce.com', 'googletagmanager.com', 'goroost.com', 'hawksearch.com', 'hawksearch.info', 'hextom.com', 'hiberniacdn.com', 'hifx.com', 'highcharts.com', 'hullapp.io', 'hwcdn.net', 'ic.com.au', 'identrust.com', 'iesnare.com', 'imedia.cz', 'imgix.net', 'imgur.com', 'insnw.net', 'instansive.com', 'investis.com', 'ipify.org', 'ipinfo.io', 'iqm.cc', 'iubenda.com', 'jifo.co', 'jotformpro.com', 'jquery.com', 'jquerytools.org', 'jsdelivr.net', 'klarna.com', 'klevu.com', 'knightlab.com', 'kxcdn.com', 'launchdarkly.com', 'leafletjs.com', 'leasewebcdn.com', 'letsencrypt.org', 'levexis.com', 'lib.showit.co', 'lightwidget.com', 'livingmap.com', 'locayta.com', 'logentries.com', 'luigisbox.com', 'matchwork.com', 'mathjax.org', 'maxmind.com', 'merchantequip.com', 'miisolutions.net', 'mlveda.com', 'mobify.net', 'money.yandex.ru', 'moovweb.net', 'mozilla.org', 'mparticle.com', 'mplxtms.com', 'msedge.net', 'msocsp.com', 'myfonts.net', 'mynewsdesk.com', 'namogoo.com', 'nccgroup.trust', 'netdna-ssl.com', 'netlifyusercontent.com', 'networksolutions.com', 'ninemsn.com.au', 'nochex.com', 'npmcdn.com', 'nr-data.net', 'o.ss2.us', 'ocsp.usertrust.com', 'okasconcepts.com', 'omguk.com', 'omniroot.com', 'onesignal.com', 'onicframework.com', 'online-metrix.net', 'onyourmap.com', 'optimahub.com', 'ostkcdn.com', 'ozcart.com.au', 'payments-amazon.com', 'paypalobjects.com', 'paysafecard.com', 'pisces-penton.com', 'pki.goog', 'placehold.it', 'po.st', 'pointp.in', 'postcodeanywhere.co.uk', 'powr.io', 'prebid.org', 'pressarea.com', 'pressjack.com', 'prezi.com', 'printfriendly.com', 'public-trust.com', 'pusherapp.com', 'pxi.pub', 'quovadisglobal.com', 'rambler.ru', 'rapidapi.com', 'rapidssl.com', 'ravelin.com', 'rawgit.com', 'raygun.io', 'realtime.co', 'recaptcha.net', 'receiptful.com', 'recollect.net', 'resrc.it', 'revenueconduit.com', 'revv.co', 'riskified.com', 'romancart.com', 'rss2json.com', 'sagepay.com', 'sajari.com', 'scanalert.com', 'scroll.com', 'searchspring.net', 'secomapp.com', 'sectigo.com', 'securitymetrics.com', 'sentry-cdn.com', 'shopgate.com', 'shopifycdn.com', 'shopkeepertools.com', 'shopstorm.com', 'siftscience.com', 'signifyd.com', 'siteblindado.com', 'siteimproveanalytics.com', 'sitetagger.co.uk', 'sli-spark.com', 'snap.licdn.com', 'sooqr.com', 'squarespace-cdn.com', 'squixa.net', 'srip.net', 'ss2.us', 'stackpile.io', 'statuspage.io', 'static1.squarespace.com', 'static.parastorage.com', 'static.showit.co', 'static.wixstatic.com', 'stormcontainertag.com', 'strands.com', 'stripe.com', 'stripe.network', 'sumologic.com', 'sunriseintegration.com', 'swiftypecdn.com', 'symcd.com', 'tagcommander.com', 'tagmanager.coremetrics.com', 'tagsrvcs.com', 'tealiumiq.com', 'telephonesky.com', 'thawte.com', 'thebrighttag.com', 'thinglink.com', 'tinyurl.com', 'transifex.com', 'travelex.co.uk', 'trust-guard.com', 'trustarc.com', 'truste.com', 'trustedshops.com', 'trustev.com', 'trustwave.com', 'turbobytes.net', 'turnto.com', 'twitframe.com', 'typekit.net', 'typography.com', 'ubertags.com', 'ucs.su', 'uploads-ssl.webflow.com', 'usablenet.net', 'v12finance.com', 'verisign.com', 'vidyard.com', 'virtualearth.net', 'visualstudio.com', 'warpcache.net', 'webink.com', 'webkul.com', 'webmarked.net', 'websiteprotection.com', 'webtype.com', 'windowsupdate.com', 'wisepops.com', 'woosmap.com', 'worldpay.com', 'wsimg.com', 'wufoo.com', 'www.gstatic.com', 'yabidos.com', 'yastatic.net', 'yopify.com', 'youramigo.com', 'zapper.com', '105app.com', '109.109.138.174', '121d8.com', '185.2.100.179', '301network.com', '365dm.com', '365webservices.co.uk', '5milesapp.com', '5min.com', '9msn.com.au', 'aabacosmallbusiness.com', 'accuweather.com', 'ada.support', 'adaptive.co.uk', 'adcmps.com', 'addthisevent.com', 'adecs.co.uk', 'adobe.com', 'adrianquevedo.com', 'agilitycms.com', 'alphr.com', 'ampproject.org', 'answerdash.com', 'aperfectpocketdata.com', 'aph.com', 'api.usehero.com', 'ardentcreative.co.uk', 'arnoldclark.com', 'assets-cdk.com', 'atlasrtx.com', 'atomvault.net', 'axs.com', 'begun.ru', 'bing.com', 'bitgravity.com', 'boldchat.com', 'bonniercorp.com', 'box.com', 'bstatic.com', 'builder.io', 'businesscatalyst.com', 'camads.net', 'cartstack.com', 'cdn.usehero.com', 'cdnds.net', 'cdnslate.com', 'channel.me', 'chatwoot.com', 'civiccomputing.com', 'clearrise.com', 'click4assistance.co.uk', 'clickability.com', 'clicktripz.com', 'clikpic.com', 'cloudinary.com', 'cnbc.com', 'cnetcontent.com', 'comm100.com', 'condenast.co.uk', 'connectevents.com.au', 'connextra.com', 'contactatonce.com', 'contentmedia.eu', 'contentreserve.com', 'conviva.com', 'coral.coralproject.net', 'covet.pics', 'cpex.cz', 'creative-serving.com', 'creators.co', 'crisp.chat', 'ctscdn.com', 'd1af033869koo7.cloudfront.net', 'd1gwclp1pmzk26.cloudfront.net', 'd1va5oqn59yrvt.cloudfront.net', 'd1w78njrm56n7g.cloudfront.net', 'd36mpcpuzc4ztk.cloudfront.net', 'd3701cc9l7v9a6.cloudfront.net', 'd3j0zfs7paavns.cloudfront.net', 'd3l7tj34e9fc43.cloudfront.net', 'dailymail.co.uk', 'dailymotion.com', 'dashhudson.com', 'datahc.com', 'dcslsoftware.com', 'dealer.com', 'dealtime.com', 'demandware.edgesuite.net', 'digitallook.com', 'dm.gg', 'dmcdn.net', 'dmtracker.com', 'dowjoneson.com', 'drct2u.com', 'drift.click', 'drift.com', 'driftt.com', 'driving.co.uk', 'dynamicyield.com', 'e-travel.com', 'ectnews.com', 'ecustomeropinions.com', 'edge-cdn.net', 'editmysite.com', 'edot.co.za', 'ehosts.net', 'elastera.net', 'emap.com', 'embed.ly', 'episerver.net', 'etouches.com', 'eventbrite.co.uk', 'everestjs.net', 'evolvemediallc.com', 'evq1.com', 'expedia.ca', 'expedia.co.jp', 'expedia.co.uk', 'expedia.com', 'expedia.com.au', 'expedia.de', 'expedia.fr', 'expedia.it', 'f3d.io', 'filepicker.io', 'flowplayer.org', 'foursixty.com', 'freespee.com', 'freetobook.com', 'fstech.co.uk', 'fuel451.com', 'fwmrm.net', 'gdgt.com', 'getmein.com', 'gettyimages.co.uk', 'gforcesinternal.co.uk', 'giphy.com', 'glassdoor.com', 'global-e.com', 'gnatta.com', 'goodlayers2.com', 'google.', 'googlevideo.com', 'goshowoff.com', 'gotraffic.net', 'greatmagazines.co.uk', 'groovygecko.net', 'gsipartners.com', 'gumtree.com', 'hatena.ne.jp', 'hbpl.co.uk', 'helpscout.net', 'hotmart.com', 'iadvize.com', 'ibpxl.com', 'idio.co', 'ifactory.com', 'ifdnrg.com', 'images-blogger-opensocial.googleusercontent.com', 'imallcdn.net', 'imgsafe.org', 'inbenta.com', 'incisivemedia.com', 'indeed.com', 'influid.co', 'inktel.com', 'inside-graph.com', 'instaembedder.com', 'intercom.io', 'intilery-analytics.com', 'ipage.com', 'iperceptions.com', 'issue.by', 'isu.pub', 'iwantthatflight.com.au', 'jd.com', 'jivosite.com', 'jobvite.com', 'jpress.co.uk', 'jwplayer.com', 'kaltura.com', 'kelkoo.com', 'klick2contact.com', 'leboncoin.fr', 'lengow.com', 'likelihood.com', 'likeshop.me', 'livebookings.com', 'livechat-static.com', 'livefyre.com', 'livehelpnow.net', 'livetex.ru', 'looper.com', 'lpsnmedia.net', 'mapbox.com', 'maps-api-ssl.google.com', 'maps.google.com', 'maps.googleapis.com', 'maps.gstatic.com', 'maptive.com', 'marketwatch.com', 'medium.com', 'meltwaternews.com', 'merchenta.com', 'metadsp.co.uk', 'metoffice.gov.uk', 'minicabit.com', 'mirror.co.uk', 'mobimanage.com', 'momondo.dk', 'momondo.net', 'momondogroup.com', 'monkeyfrogmedia.com', 'mts.googleapis.com', 'mtvnservices.com', 'mymovies.net', 'mywebsitebuilder.com', 'mzstatic.com', 'nanorep.com', 'navistechnologies.info', 'netop.com', 'newsinc.com', 'newsquestdigital.co.uk', 'nexcesscdn.net', 'nflximg.net', 'nitrosell.com', 'nmm.de', 'nonprofitsoapbox.com', 'northernandshell.co.uk', 'nrelate.com', 'nscontext.eu', 'odistatic.net', 'olark.com', 'onmodulus.net', 'openstreetmap.org', 'opentok.com', 'opta.net', 'p-td.com', 'peer1.com', 'performgroup.com', 'periscope.tv', 'photobucket.com', 'photorank.me', 'playbuzz.com', 'player.vimeo.com', 'plentific.com', 'pmc.com', 'postimg.org', 'prefixbox.com', 'premiumtv.co.uk', 'pricegrabber.com', 'pricerunner.com', 'primefuse.com', 'projects.fm', 'proper.io', 'propertyweek.com', 'providesupport.com', 'proweb.net', 'psplugin.com', 'pubfactory.com', 'publishme.se', 'purechat.com', 'pxlad.io', 'qodeinteractive.com', 'quartalflife.com', 'reachmee.com', 'recruitmentplatform.com', 'researchonline.org.uk', 'resources.fairfax.com.au', 'revcontent.com', 'rnengage.com', 'rnkr-static.com', 'roomkey.com', 's-9.us', 'sabio.co.uk', 'salesforceliveagent.com', 'samba.tv', 'sara.media', 'scdn.co', 'scrvt.com', 'sekindo.com', 'selectmedia.asia', 'servebom.com', 'shld.net', 'shopatron.com', 'shopifysvc.com', 'shopmania.com', 'silktide.com', 'simplestream.com', 'skyscanner.net', 'slideshare.com', 'smartassistant.com', 'smartertrack.com', 'smartsuppcdn.com', 'smartwebportal.co.uk', 'smh.com.au', 'snack-media.com', 'snapengage.com', 'snapwidget.com', 'socialannex.com', 'softwebzone.com', 'sorensonmedia.com', 'soticservers.net', 'soundcloud.com', 'spotify.com', 'squarespace.com', 'staticflickr.com', 'stratus.sc', 'stumbleupon.com', 'sublimevideo.net', 'synthetix.com', 'taleo.net', 'tawk.to', 'template-help.com', 'thcdn.com', 'thefind.com', 'thelocalpeople.co.uk', 'tidiochat.com', 'tildacdn.com', 'timeinc.net', 'tmcs.net', 'tomandco.uk', 'toptable.co.uk', 'touchcommerce.com', 'track-mv.com', 'travelocity.ca', 'travelocity.com', 'travelzoo.com', 'tripadvisor.co.uk', 'ttgtmedia.com', 'tutorialize.me', 'tvgenius.net', 'twenga.co.uk', 'twentythree.net', 'twitch.tv', 'typeform.com', 'typepad.com', 'uciservice.com', 'uicdn.com', 'uimserv.net', 'uk-plc.net', 'uplynk.com', 'usersnap.com', 'vee24.com', 'veeseo.com', 'verestads.net', 'vergic.com', 'viamichelin.com', 'vimeocdn.com', 'vioapi.com', 'vivocha.com', 'voxmedia.com', 'walkme.com', 'webcollage.net', 'webphone.net', 'webselect.net', 'websitealive7.com', 'websitetestlink.com', 'webthinking.co.uk', 'webvideocore.net', 'whoson.com', 'widearea.co.uk', 'widgets.wp.com', 'willyfogg.com', 'wistia.net', 'wixapps.net', 'wnmedia.co.uk', 'workcast.net', 'wpengine.com', 'wrbm.com', 'wsj.net', 'xlcdn.com', 'xmlshop.biz', 'yelp.com', 'yfrog.com', 'yottaa.net', 'youtube-nocookie.com', 'youtube.com', 'ytimg.com', 'yudu.com', 'ywxi.net', 'zencdn.net', 'zergnet.com', 'zerogrey.com', 'zopim.com', 'zopim.io', 'ztat.net', 'addthis.com', 'addthisedge.com', 'addtoany.com', 'ahalogy.com', 'atlassbx.com', 'audioboo.fm', 'beetailer.com', 'breakingburner.com', 'bufferapp.com', 'buzzfed.com', 'bwbx.io', 'ccm2.net', 'cdninstagram.com', 'cint.com', 'clickable.net', 'daumcdn.net', 'delicious.com', 'directededge.com', 'disqus.com', 'disquscdn.com', 'donreach.com', 'dsms0mj1bbhn4.cloudfront.net', 'facebook.com', 'fbcdn-photos-e-a.akamaihd.net', 'fbcdn.net', 'fbsbx.com', 'flipboard.com', 'flockler.com', 'geckotribe.com', 'getsocial.io', 'gravatar.com', 'icnetwork.co.uk', 'instagram.com', 'ipstatp.com', 'jtdiscuss.com', 'lessbuttons.com', 'lfstmedia.com', 'linkedin.com', 'livejournal.net', 'loginradius.com', 'metabroadcast.com', 'mobilenations.com', 'mshcdn.com', 'myspace.com', 'news-static.com', 'newsharecounts.com', 'pinterest.com', 'pistonheads.com', 'pixlee.com', 'pixnet.net', 'plus.google.com', 'poweringnews.com', 'qrius.me', 'redditstatic.com', 'rssinclude.com', 'sentifi.com', 'sharebutton.co', 'sharethis.com', 'shop.pe', 'shopapps.in', 'slidesharecdn.com', 'slpht.com', 'socialshopwave.com', 'spotim.market', 'sstatic.net', 'stackla.com', 'storify.com', 'syndication.twitter.com', 't.co', 'tagboard.com', 'thebestday.com', 'tru.am', 'tumblr.com', 'twitter.com', 'vk.com']

url1 = "https://cookiepedia.co.uk/host/"

with open("cookies.csv", "a", newline="") as file:
    writer = csv.writer(file)
    # writer.writerow(["Website URL", "Cookie Names","Domain","Host", "Purpose", "Description", "Cookie URL","Is Secure","Is HTTP only?","Path"])

    for link in links:
        try:
            LINK = url1+link
            data1 = req(LINK)
            print(LINK)
            print(data1)
            for entries in data1:
                entries = list(entries.split(","))
                dict1 = {entries[i]: entries[i + 1] for i in range(0, len(entries) - 1, 2)}
                create_entry(dict1, LINK)
        except:
            pass
