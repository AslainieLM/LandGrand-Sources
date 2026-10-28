param(
  [Parameter(Mandatory=$true)][string]$InputDocx,
  [Parameter(Mandatory=$true)][string]$OutputPdf,
  [Parameter(Mandatory=$true)][string]$AuditJson
)
$ErrorActionPreference = 'Stop'
$wordRenderApp = $null
$wordRenderDoc = $null
try {
  $wordRenderApp = New-Object -ComObject Word.Application
  $wordRenderApp.Visible = $false
  $wordRenderApp.DisplayAlerts = 0
  $wordRenderApp.AutomationSecurity = 3
  $wordRenderDoc = $wordRenderApp.Documents.Open($InputDocx, $false, $true, $false)
  $wordRenderDoc.Repaginate()
  $wordRenderDoc.ExportAsFixedFormat($OutputPdf, 17)
  $wordRenderParagraphs = @()
  foreach ($wordParagraph in $wordRenderDoc.Paragraphs) {
    $wordParagraphText = $wordParagraph.Range.Text.Trim([char]13,[char]7)
    if ($wordParagraphText.Length -gt 0) {
      $wordStartRange = $wordParagraph.Range.Duplicate
      $wordStartRange.Collapse(1)
      $wordRenderParagraphs += [PSCustomObject]@{
        text = $wordParagraphText
        startPage = $wordStartRange.Information(3)
        endPage = $wordParagraph.Range.Information(3)
      }
      [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordStartRange) | Out-Null
    }
  }
  [PSCustomObject]@{
    engine = 'Microsoft Word'
    wordVersion = $wordRenderApp.Version
    readOnly = $wordRenderDoc.ReadOnly
    pages = $wordRenderDoc.ComputeStatistics(2)
    words = $wordRenderDoc.ComputeStatistics(0)
    lines = $wordRenderDoc.ComputeStatistics(1)
    characters = $wordRenderDoc.ComputeStatistics(3)
    charactersWithSpaces = $wordRenderDoc.ComputeStatistics(5)
    paragraphCount = $wordRenderDoc.ComputeStatistics(4)
    paragraphs = $wordRenderParagraphs
  } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $AuditJson -Encoding utf8
  [PSCustomObject]@{pdf=$OutputPdf;pages=$wordRenderDoc.ComputeStatistics(2);audit=$AuditJson} | ConvertTo-Json
} finally {
  if ($null -ne $wordRenderDoc) {
    $wordRenderDoc.Close(0)
    [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordRenderDoc) | Out-Null
  }
  if ($null -ne $wordRenderApp) {
    $wordRenderApp.Quit(0)
    [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordRenderApp) | Out-Null
  }
}
