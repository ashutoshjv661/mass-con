#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Created by Ashutosh Jadhav . 
# Google codein 2014
import string
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

class fromMenu(wx.Menu):
    
    def __init__(self, parent):
        super(fromMenu, self).__init__()
        self.units = ["kg","tonne","ounce","Pound","carat"]
        self.parent = parent
        
        for unit in self.units:
            item = wx.MenuItem(self, wx.NewId(), unit)
            self.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnFromUnitSelected, item)
    def OnFromUnitSelected(self,event):
        fromUnit = self.FindItemById(event.GetId())
        text = fromUnit.GetText()
        ## set "From ___" label
        fromText.SetLabel("From %s"% text)
        
        toUnitText = toText.GetLabel().split(" ")[1]
        fromTo = text + "_" + toUnitText
        ## if text is only digits, then convert and display result
        try:
            fromFloat = float(fromEnter.GetValue())
            toString = str(fromFloat * conversionFactors[fromTo])
            toEnter.SetValue(toString)
        except ValueError:
            toEnter.SetValue("Only Enter Digits")

            

class toMenu(wx.Menu):
    
    def __init__(self, parent):
        super(toMenu, self).__init__()
        self.units = ["kg","tonne","ounce","Pound","carat"]
        self.parent = parent
        
        for unit in self.units:
            item = wx.MenuItem(self, wx.NewId(), unit)
            self.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnToUnitSelected, item)
            
    def OnToUnitSelected(self,event):
        toUnit = self.FindItemById(event.GetId())
        text = toUnit.GetText()
        
        ## set "To ___" label to correct unit
        toText.SetLabel("To %s"% text)
        
        fromUnitText = fromText.GetLabel().split(" ")[1]
        fromTo=fromUnitText + "_" + text
        

        ## if text is only digits, then convert and display result
        try:
            fromFloat = float(fromEnter.GetValue())
            toString = str(fromFloat * conversionFactors[fromTo])
            toEnter.SetValue(toString)
        except ValueError:
            toEnter.SetValue("Error")

class massConvert(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.parent = parent
        self.initialize()
    def initialize(self):
        ## Conversion Factors using "From_To" as key to multiply by
        global conversionFactors
        conversionFactors = {"kg_kg":1,"tonne_kg":1000,"ounce_kg":0.028349523125,"Pound_kg":0.45359237,"carat_kg":0.0002,
                                "kg_tonne":0.001,"tonne_tonne":1,"ounce_tonne":0.000028349523125,"Pound_tonne":0.00045359237,"carat_tonne":0.0000002,
                                "kg_ounce":35.27396194958041,"tonne_ounce":35273.96194958041,"ounce_ounce":1,"pound_ounce":16,"carat_ounce":0.0070547923899161,
                                "kg_Pound":2.204622621848776,"tonne_Pound":2204.622621848776,"ounce_pound":0.0625,"Pound_Pound":1,"carat_Pound":4.409245243697552e-4,
                                "kg_carat":5000,"tonne_carat":5000000,"ounce_carat":141.747615625,"Pound_carat":2267.96185,"carat_carat":1}
        self.units = ["kg","tonne","ounce","Pound","carat"]
        global fromTo
        fromTo="kg_kg"

        panel = wx.Panel(self)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        fgs = wx.FlexGridSizer(3, 3, 9, 25)

        global fromText
        fromText = wx.Button(panel, id=0, label="From kg")
        
        global toText
        toText = wx.Button(panel, id=-1, label="To kg")
        self.Bind(wx.EVT_BUTTON, self.OnToFromTextSelected)
        
        global fromEnter
        fromEnter = wx.TextCtrl(panel, -1, style=wx.TE_PROCESS_ENTER)
        ## Bind typing enter from text box to updating the returned conversion
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterKeyPress)
        
        global toEnter
        toEnter = wx.TextCtrl(panel,3,style=wx.TE_READONLY)
        
        fgs.AddMany([(fromText), (wx.StaticText(panel),1,wx.EXPAND), (toText), 
            (fromEnter, 1, wx.EXPAND), (wx.StaticText(panel, label="=")), (toEnter, 1, wx.EXPAND),
            (wx.StaticText(panel),1,wx.EXPAND),(wx.StaticText(panel),1,wx.EXPAND),(wx.StaticText(panel),1,wx.EXPAND)])
        
        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)
        
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)
        self.SetSize((275,100))
        self.Show(True)
        
    def OnEnterKeyPress(self, event):
        fromTo = (fromText.GetLabel().split(" ")[1]) + "_" + toText.GetLabel().split(" ")[1]
        try:
            fromFloat = float(fromEnter.GetValue())
            toString = str(fromFloat * conversionFactors[fromTo])
            toEnter.SetValue(toString)
        except ValueError:
            toEnter.SetValue("Error")
            
    def OnToFromTextSelected(self,event):
        buttonID = event.GetId()
        buttonByID = self.FindWindowById(buttonID)
        buttonStartText = buttonByID.GetLabel().split(" ")[0]
        
        ## Check if Button Label is "To" or "From" and handle menu appropriately
        if buttonStartText == "From":
            self.PopupMenu(fromMenu(self), (25,10))
        elif buttonStartText == "To":
            self.PopupMenu(toMenu(self), (195,10))
            
if __name__ == "__main__":
    app = wx.App()
    frame = massConvert(None,-1,'Mass Converter [By:-Ashutosh Jadhav(ashutoshjadhav661@gmail.com)]')
    app.MainLoop()
