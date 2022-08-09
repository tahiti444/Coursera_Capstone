# -*- coding: utf-8 -*-

from classes.logger import *
from classes.chartography import *
from classes.foursquare import *
import pytest


def test_country_equals_germany():
    assert CenteredChart().country != "Spain"


def test_draw_wismar_on_map():
    map1 = CenteredChart()
    map1.setFeatureGroup()
    map1.drawPoint("54", "11", "test")
    map1.saveMap(path="./test/popupmap.html")


def test_url():
    link1 = Link().venue(
        query="Automation",
        location="54.083,12.133",
        client_id="P1YQAFRAQSNTLIX1ZSRRLUDXB2JGT0KPNSPGFBWXOMBVL4X4",
        client_secret="HEADURYPNTU24PWKRJADVLS5OMSOU0XKKN4H5F4E5YYFUZJ1",
    )
    assert (
        link1
        == "https://api.foursquare.com/v2/venues/search?ll=54.083,12.133&query=Automation&client_id=P1YQAFRAQSNTLIX1ZSRRLUDXB2JGT0KPNSPGFBWXOMBVL4X4&client_secret=HEADURYPNTU24PWKRJADVLS5OMSOU0XKKN4H5F4E5YYFUZJ1&v=20180602"
    )


def test_header():
    link1 = Link()
    link1.venue(
        query="Automation",
        location="54.083,12.133",
        client_id="P1YQAFRAQSNTLIX1ZSRRLUDXB2JGT0KPNSPGFBWXOMBVL4X4",
        client_secret="HEADURYPNTU24PWKRJADVLS5OMSOU0XKKN4H5F4E5YYFUZJ1",
    )
    link1.getResponse()
    if link1.hasError():
        print("web response throw an error: " + str(link1.getError()))
    assert link1.hasError() is False

