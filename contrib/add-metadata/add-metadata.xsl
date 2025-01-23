<?xml version="1.0" encoding="UTF-8"?>
<!--
    Purpose:
       Add missing SUSE metadata into <info> tag

    Prerequisites:
       * A XSLT 1.0 processor
       * If you want to preserve entities in your text, mask them before you apply the
         stylesheets

    Behaviour:
       The stylesheet looks if a specific meta tag is available. If it's available,
       it copies the tag to the result tree unchanged.
       If the respective tag is not available, the stylesheet creates the tag in the
       result tree. In some cases you can pass a parameter to add the content (text or
       child elements) to the tag.

    Parameters for meta tags content:
      * meta-arch: Comma separated list of architectures to add for <meta name="architecture">
      * meta-category: Comma separated list of categories to add for <meta name="category">
      * meta-series: String to add for <meta name="series">
      * meta-task: Comma separated list of tasks to add for <meta name="task">
      * meta-type: String to add for <meta name="type">

    Parameters for enabling/disabling meta tags:
      * use-meta-arch: Enable/disable <meta name="arch">
      * use-meta-category: Enable/disable <meta name="series">
      * use-meta-description: Enable/disable <meta name="description">
      * use-meta-series: Enable/disable <meta name="series">
      * use-meta-task: Enable/disable <meta name="task">
      * use-meta-type: Enable/disable <meta name="type">

    General Parameters:
      * delim: The delimiter used to separate each parameter (by default ",")
      * default-text: The default text to use when we create an element with text
-->

<xsl:stylesheet version="1.0"
  xmlns="http://docbook.org/ns/docbook"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:its="http://www.w3.org/2005/11/its"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 >

  <xsl:output method="xml"/>

  <!-- ==== Content Parameters -->
  <xsl:param name="meta-arch" />
  <xsl:param name="meta-category" />
  <xsl:param name="meta-series" />
  <xsl:param name="meta-task" />
  <xsl:param name="meta-title" />
  <xsl:param name="meta-type" />

  <!-- ==== Boolean Parameters -->
  <xsl:param name="use-meta-arch" select="false()" />
  <xsl:param name="use-meta-category" select="true()" />
  <xsl:param name="use-meta-description" select="true()" />
  <xsl:param name="use-meta-platform" select="true()" />
  <xsl:param name="use-meta-series" select="true()" />
  <xsl:param name="use-meta-task" select="true()" />
  <xsl:param name="use-meta-title" select="true()" />
  <xsl:param name="use-meta-type" select="false()" />

  <xsl:param name="delim">,</xsl:param>
  <xsl:param name="default-text">FIXME</xsl:param>

  <!-- ==== Copy nodes -->
  <xsl:template match="node() | @*" name="copy">
  <xsl:copy>
    <xsl:apply-templates select="@* | node()"/>
  </xsl:copy>
</xsl:template>


  <!-- ==== Templates -->
  <xsl:template match="d:info|d:merge">
    <xsl:copy>
      <xsl:copy-of select="@*"/>
      <!-- Copy all element excluding meta elements -->
      <xsl:apply-templates select="*[not(self::d:meta)]"/>
      <xsl:text>&#10;&#10;</xsl:text>
      <xsl:comment> SUSE Metadata Start</xsl:comment>
      <xsl:text>&#10;</xsl:text>

      <xsl:call-template name="meta-architecture" />
      <xsl:call-template name="meta-category" />
      <xsl:call-template name="meta-description" />
      <xsl:call-template name="meta-series" />
      <xsl:call-template name="meta-social-descr" />
      <xsl:call-template name="meta-task" />
      <xsl:call-template name="meta-title" />
      <xsl:call-template name="meta-type" />

      <xsl:text>&#10;</xsl:text>
      <xsl:comment> SUSE Metadata End</xsl:comment>
      <xsl:text>&#10;</xsl:text>
    </xsl:copy>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>


  <!-- ==== Helper templates -->
  <xsl:template name="split-string">
    <xsl:param name="list"/>
    <xsl:param name="delimiter" select="$delim"/>

    <xsl:choose>
      <xsl:when test="contains($list, $delimiter)">
        <!-- Extract the first token -->
        <xsl:variable name="token" select="substring-before($list, $delimiter)"/>

        <!-- Process the current token -->
        <xsl:call-template name="wrap-token">
          <xsl:with-param name="token" select="$token"/>
        </xsl:call-template>

        <!-- Recursively call splitString with the remaining part of the list -->
        <xsl:call-template name="split-string">
          <xsl:with-param name="list" select="substring-after($list, $delimiter)"/>
          <xsl:with-param name="delimiter" select="$delimiter"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <!-- Process the last token -->
        <xsl:call-template name="wrap-token">
          <xsl:with-param name="token" select="$list"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <!-- Template to wrap a token in a phrase tag -->
  <xsl:template name="wrap-token">
    <xsl:param name="token"/>

    <phrase><xsl:value-of select="$token"/></phrase>
  </xsl:template>

  <!-- ==== Named templates -->
  <xsl:template name="meta-architecture">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='architecture']">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="d:meta[@name='architecture']"/>
      </xsl:when>
      <xsl:when test="boolean($use-meta-arch)">
        <xsl:text>&#10;</xsl:text>
        <meta name="architecture" its:translate="no">
          <xsl:choose>
            <xsl:when test="$meta-arch != ''">
              <xsl:call-template name="split-string">
                <xsl:with-param name="list" select="$meta-arch" />
              </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <phrase><xsl:value-of select="$default-text" /></phrase>
            </xsl:otherwise>
          </xsl:choose>
        </meta>
      </xsl:when>
      <xsl:otherwise />
    </xsl:choose>
  </xsl:template>

  <xsl:template name="meta-category">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='category']">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="d:meta[@name='category']"/>
      </xsl:when>
      <xsl:when test="boolean($use-meta-category)">
        <xsl:text>&#10;</xsl:text>
        <meta name="category" its:translate="no">
          <xsl:choose>
            <xsl:when test="$meta-category != ''">
              <xsl:call-template name="split-string">
                <xsl:with-param name="list" select="$meta-category" />
              </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <phrase><xsl:value-of select="$default-text" /></phrase>
            </xsl:otherwise>
          </xsl:choose>
        </meta>
      </xsl:when>
      <xsl:otherwise />
    </xsl:choose>
  </xsl:template>

  <xsl:template name="meta-description">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='description']">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="d:meta[@name='description']"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;</xsl:text>
        <meta name="description" its:translate="yes">
          <xsl:value-of select="$default-text"/>
        </meta>
        <xsl:text>&#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="meta-series">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='series']">
        <xsl:apply-templates select="d:meta[@name='series']"/>
      </xsl:when>
      <xsl:otherwise>
        <meta name="series" its:translate="no">
          <xsl:choose>
            <xsl:when test="$meta-series != ''">
              <xsl:value-of select="$meta-series"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="$default-text"/>
            </xsl:otherwise>
          </xsl:choose>
        </meta>
        <xsl:text>&#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="meta-social-descr">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='social-descr']">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="d:meta[@name='social-descr']"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;</xsl:text>
        <meta name="social-descr" its:translate="yes">
          <xsl:value-of select="$default-text"/>
        </meta>
        <xsl:text>&#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="meta-task">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='task']">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="d:meta[@name='task']"/>
      </xsl:when>
      <xsl:when test="boolean($use-meta-task)">
        <xsl:text>&#10;</xsl:text>
        <meta name="task" its:translate="yes">
          <xsl:choose>
            <xsl:when test="$meta-task != ''">
              <xsl:call-template name="split-string">
                <xsl:with-param name="list" select="$meta-task" />
              </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <phrase><xsl:value-of select="$default-text" /></phrase>
            </xsl:otherwise>
          </xsl:choose>
        </meta>
        <xsl:text>&#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise />
    </xsl:choose>
  </xsl:template>

  <xsl:template name="meta-title">
    <xsl:param name="node" select="."/>
  </xsl:template>

  <xsl:template name="meta-type">
    <xsl:param name="node" select="."/>
    <xsl:choose>
      <xsl:when test="d:meta[@name='type']">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="d:meta[@name='type']"/>
      </xsl:when>
      <xsl:when test="boolean($use-meta-type)">
        <xsl:text>&#10;</xsl:text>
        <meta name="type" its:translate="no">
          <xsl:choose>
            <xsl:when test="$meta-type != ''">
              <xsl:value-of select="$meta-type"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="$default-text" />
            </xsl:otherwise>
          </xsl:choose>
        </meta>
      </xsl:when>
      <xsl:otherwise/>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>