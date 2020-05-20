<?xml version="1.0" encoding="UTF-8"?>
<!--
   Purpose:
     Post-process a DocBook document produced by AsciiDoctor

   Parameters:
     None

   Input:
     A DocBook 5 document

   Output:
     Changed DocBook 5 document

     Currently, the following corrections are made:
     * simpara -> para
       * allows GeekoDoc validation
       * suse2013 =< 2.0.12 display improvement
     * sidebar -> note
       * allows GeekoDoc validation
       * suse2013 display improvement
     * literallayout[@class='monospaced'] -> screen
       * allows GeekoDoc validation
       * suse2013 layout improvement
     * info + abstract -> info/abstract
       * allows DocBook validation
     * article/info/title -> article/title
       * suse2013 =< 2.0.13 display improvement, suse-xsl#397

   Author:    Thomas Schraitle <toms@opensuse.org>
   Copyright (C) 2018 SUSE Linux GmbH

-->
<!DOCTYPE xsl:stylesheet
[
   <!ENTITY db5ns "http://docbook.org/ns/docbook">
]>
<xsl:stylesheet version="1.0"
 xmlns:d="&db5ns;"
 xmlns="&db5ns;"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="../common/copy.xsl"/>
 <xsl:output indent="yes"/>

 <!-- Not supported in GeekoDoc -->
 <xsl:template match="authorinitials"/>

 <xsl:template match="d:guibutton|d:guimenuitem|d:guisubmenu">
   <xsl:element name="guimenu" namespace="&db5ns;">
    <xsl:copy-of select="@*"/>
    <xsl:apply-templates/>
   </xsl:element>
 </xsl:template>

 <xsl:template match="d:sidebar">
   <xsl:element name="note" namespace="&db5ns;">
    <xsl:copy-of select="@*"/>
    <xsl:apply-templates/>
   </xsl:element>
 </xsl:template>

 <xsl:template match="d:simpara">
  <xsl:element name="para" namespace="&db5ns;">
   <xsl:copy-of select="@*"/>
   <xsl:apply-templates/>
  </xsl:element>
 </xsl:template>

 <xsl:template match="d:literallayout[@class='monospaced']|d:programlisting">
  <xsl:element name="screen" namespace="&db5ns;">
   <xsl:copy-of select="@*[local-name()!='class']"/>
   <xsl:apply-templates/>
  </xsl:element>
 </xsl:template>

<xsl:template match="d:imagedata">
 <xsl:copy>
  <xsl:copy-of select="@*[local-name() != 'contentwidth']"/>
  <xsl:choose>
   <xsl:when test="@width">
    <xsl:copy-of select="@width"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:attribute name="width">
     <xsl:value-of select="@contentwidth"/>
    </xsl:attribute>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:copy>
</xsl:template>

<xsl:template match="d:abstract[not(ancestor::d:info)]"/>
<xsl:template match="d:info[following-sibling::d:abstract]">
  <xsl:element name="{local-name(.)}" namespace="&db5ns;">
    <xsl:apply-templates select="@*|node()"/>
    <xsl:apply-templates select="following-sibling::d:abstract" mode="copy-element"/>
  </xsl:element>
</xsl:template>

<xsl:template match="*" mode="copy-element">
  <xsl:element name="{local-name(.)}" namespace="&db5ns;">
    <xsl:apply-templates select="@*|node()"/>
  </xsl:element>
</xsl:template>

<xsl:template match="d:article/d:info/d:title"/>
<xsl:template match="d:article[d:info/d:title]">
  <xsl:element name="{local-name(.)}" namespace="&db5ns;">
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select="d:info/d:title" mode="copy-element"/>
    <xsl:apply-templates select="node()"/>
  </xsl:element>
</xsl:template>

</xsl:stylesheet>
