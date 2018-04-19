function Test-RegistryValue {

param (

 [parameter(Mandatory=$true)]
 [ValidateNotNullOrEmpty()]$Path,

[parameter(Mandatory=$true)]
 [ValidateNotNullOrEmpty()]$Value
)

try {

Get-ItemProperty -Path $Path | Select-Object -ExpandProperty $Value -ErrorAction Stop | Out-Null
 return $true
 }

catch {

return $false

}

}

function set-wallPaper ([string]$desktopImage)
{
#Write-Host $desktopImage
     Remove-ItemProperty -path "HKCU:\Control Panel\Desktop" -name WallPaper 

#Not actually needed
<#
     for ($i = 0; $i -le 5; $i++)
     { 
         if (Test-RegistryValue -path "hkcu:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Wallpapers" -value "BackgroundHistoryPath$i" )
         {
         Remove-itemproperty -path "hkcu:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Wallpapers" -name "BackgroundHistoryPath$i" 
         }
     }
#>


     set-itemproperty -path "HKCU:\Control Panel\Desktop" -name WallPaper -value $desktopImage

#needed to actually change the background consistently 

#Sleep -seconds 5

RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters 


#Not needed but lets you know it was set correctly  
#         Get-ItemProperty -path "HKCU:\Control Panel\Desktop" 
}

[void] [System.Reflection.Assembly]::LoadWithPartialName('System.drawing') 

$sourcePath = "C:\\temp\\tmpBG-from-NASA.jpg"
$destPath = "C:\temp\pod2.jpg"

$request =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

$json = Invoke-WebRequest $request | ConvertFrom-Json
$myurl = $json | select hdurl  | select -expand hdurl
$Title = $json | select title  | select -expand title

Invoke-WebRequest -Uri $myurl -OutFile $sourcePath
$srcImg = [System.Drawing.Image]::FromFile($sourcePath)
 
$bmpFile = new-object System.Drawing.Bitmap([int]($srcImg.width)),([int]($srcImg.height))

$Image = [System.Drawing.Graphics]::FromImage($bmpFile)
$Image.SmoothingMode = "AntiAlias"
 
$Rectangle = New-Object Drawing.Rectangle 0, 0, $srcImg.Width, $srcImg.Height
$Image.DrawImage($srcImg, $Rectangle, 0, 0, $srcImg.Width, $srcImg.Height, ([Drawing.GraphicsUnit]::Pixel))

$Font = new-object System.Drawing.Font("Verdana", 80)
$Brush = New-Object Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$Image.DrawString($Title, $Font, $Brush, 10, 10)

$bmpFile.save($destPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$bmpFile.Dispose()
$srcImg.Dispose()

set-wallPaper($destPath)