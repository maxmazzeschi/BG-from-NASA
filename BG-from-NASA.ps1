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
Write-Host $desktopImage
 #    Remove-ItemProperty -path "HKCU:\Control Panel\Desktop" -name WallPaper 

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

$request =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
$myurl = Invoke-WebRequest $request |
ConvertFrom-Json |
select hdurl  | select -expand hdurl

Invoke-WebRequest -Uri $myurl -OutFile "C:\\temp\\pod.jpg"
set-wallPaper("C:\temp\pod.jpg")


