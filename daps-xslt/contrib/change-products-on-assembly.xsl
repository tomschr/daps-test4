<!--
   Purpose:
     Changes the <meta name="productname"> content of an assembly file

   Parameters:
     * structure.id: The ID of the structure (<structure xml:id="ID">) to process.
                     Only needed if more than one structure is available in the assembly file.
                     Creates an error if more than one structure is there, but no structure.id is set.
     * version:      The version to add or remove in <productname version="...">
                     If not set, the stylesheet does NOT continue
     * product:      The product to add or remove in <productname version="...">...</productname>
                     If not set, the stylesheet does NOT continue
     * op:           The operation to execute:
                     - "add", "a": adds the respective structure to <meta name="productname">
                     - "remove", "rm", "r": removes the respective structure from <meta name="productname">

   Additional hints:
     Entities are resolved. If you need to preserve them, protect them first!

   Input:
     DocBook assembly document with a <meta name="productname"> element

   Output:
     A DocBook assembly document with changed metadata content in <meta name="productname">

   Author:    Tom Schraitle <toms@opensuse.org>
   Date:      2025, Jan

-->
<xsl:stylesheet version="1.0"
  xmlns="http://docbook.org/ns/docbook"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="no"/>

  <xsl:key name="id" match="*" use="@xml:id"/>

  <xsl:preserve-space elements="d:meta d:screen"/>

  <!--
    ### XSLT Parameters
  -->
  <!-- The ID of the structure (<structure xml:id="ID">) to process. -->
  <xsl:param name="structure.id" />

  <!-- The version to add or remove in <productname version="..."> -->
  <xsl:param name="version">
    <xsl:message terminate="yes">XSLT Parameter 'version' not set</xsl:message>
  </xsl:param>

  <!-- The product to add or remove in <productname version="..."> -->
  <xsl:param name="product">
    <xsl:message terminate="yes">XSLT Parameter 'product' not set</xsl:message>
  </xsl:param>

  <!-- Operation to execute: "add" or "remove" -->
  <xsl:param name="op">
    <xsl:message terminate="yes">XSLT Parameter 'op' not set</xsl:message>
  </xsl:param>

  <!-- The separator for meta.add.products and meta.remove.products to separate products
       from each other
  -->
  <xsl:param name="sep">;</xsl:param>

  <!--
    ### Templates
  -->
  <!-- Default: copy all nodes if no specific template exists -->
  <xsl:template match="node() | @*">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()" />
    </xsl:copy>
  </xsl:template>


  <xsl:template match="/*[not(self::d:assembly)]" priority="1">
    <xsl:message terminate="yes">ERROR: This document is NOT an assembly file</xsl:message>
  </xsl:template>


  <xsl:template match="/d:assembly[count(d:structure) > 1]">
    <xsl:choose>
      <xsl:when test="$structure.id = ''">
        <xsl:message terminate="yes">
          <xsl:text>ERROR: The document contains more than one structure.&#10;</xsl:text>
          <xsl:text>Choose the structure you want to change with the XSLT parameter `structure.id'. Either:&#10;</xsl:text>
          <xsl:text>1. Use the ID of the structure: structure.id="ID"&#10;</xsl:text>
          <xsl:text>2. Use structure.id='#all' to change all &lt;structure>s in the assembly.</xsl:text>
        </xsl:message>
      </xsl:when>
      <xsl:when test="$structure.id = '#all'">
        <xsl:apply-templates />
      </xsl:when>
      <xsl:when test="count(key('id', $structure.id))">
        <xsl:message terminate="yes">
          <xsl:text>ERROR: ID '</xsl:text>
          <xsl:value-of select="$structure.id"/>
          <xsl:text>' not found in assembly.</xsl:text>
        </xsl:message>
      </xsl:when>
      <xsl:otherwise>
        <xsl:message>INFO: Selecting structure <xsl:value-of select="concat('&quot;', $structure.id, '&quot;')"/></xsl:message>
        <xsl:apply-templates select="node()[self::d:structure[@xml:id != $structure.id]]" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>


  <xsl:template match="d:structure[d:merge[count(d:meta[@name = 'productname']) = 0]]" priority="1">
    <xsl:message>WARNING: No &lt;meta name="productname"> found in structure<xsl:value-of
      select="concat('[@xml:id=&quot;', @xml:id, '&quot;]')"/></xsl:message>
    <xsl:apply-templates />
  </xsl:template>


  <xsl:template match="d:meta[@name = 'productname']">
    <xsl:variable name="productnames" select="d:productname[@version = $version][normalize-space(.) = $product]"/>
    <xsl:variable name="op-norm">
      <xsl:choose>
        <xsl:when test="$op = 'a'">add</xsl:when>
        <xsl:when test="$op = 'r'">remove</xsl:when>
        <xsl:when test="$op = 'rm'">remove</xsl:when>
        <xsl:otherwise><xsl:value-of select="$op"/></xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:message>INFO: Found &lt;meta name="productname"></xsl:message>
    <xsl:message>INFO: Found productnames for
      version = <xsl:value-of select="$version"/>
      product = <xsl:value-of select="$product"/>
      => <xsl:value-of select="count($productnames)"/>
    </xsl:message>
    <xsl:copy>
      <xsl:apply-templates select="@*" />
      <xsl:choose>
        <xsl:when test="$op-norm = 'add' and count($productnames) = 0">
          <xsl:message>INFO: Adding &lt;productname version="<xsl:value-of
            select="$version"/>"><xsl:value-of select="$product"/>&lt;/productname></xsl:message>
          <xsl:apply-templates />
          <productname version="{$version}"><xsl:value-of select="normalize-space($product)"/></productname>
          <xsl:text>&#10;</xsl:text>
        </xsl:when>
        <xsl:when test="$op-norm = 'add' and count($productnames) != 0">
          <xsl:message>WARNING: The &lt;productname version="<xsl:value-of
            select="$version"/>"><xsl:value-of select="$product"/>&lt;/productname> already exists</xsl:message>
          <xsl:apply-templates />
        </xsl:when>
        <xsl:when test="$op-norm = 'remove' and count($productnames) = 0">
          <xsl:message>WARNING: Cannot remove &lt;productname version="<xsl:value-of
            select="$version"/>"><xsl:value-of select="$product"/>&lt;/productname>; does NOT exist</xsl:message>
          <xsl:apply-templates />
        </xsl:when>
        <xsl:when test="$op-norm = 'remove' and count($productnames) = 1">
          <xsl:message>INFO: Removing &lt;productname version="<xsl:value-of
            select="$version"/>"><xsl:value-of select="$product"/>&lt;/productname></xsl:message>
          <xsl:apply-templates select="*[not(self::productname[@version=$version][normalize-space(.) = $product])]" />
        </xsl:when>
        <xsl:otherwise>
          <xsl:message>Is this correct? Should that be happen?</xsl:message>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>