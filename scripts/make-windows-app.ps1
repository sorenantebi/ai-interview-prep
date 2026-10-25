# Adds a "prep" shortcut (with the app icon) to the Start Menu and Desktop. Pin it to the taskbar from the Start Menu.
$root = Split-Path -Parent $PSScriptRoot
$shell = New-Object -ComObject WScript.Shell
foreach ($dir in @([Environment]::GetFolderPath("Programs"), [Environment]::GetFolderPath("Desktop"))) {
  $s = $shell.CreateShortcut((Join-Path $dir "prep.lnk"))
  $s.TargetPath = Join-Path $root "scripts\launch.cmd"
  $s.WorkingDirectory = $root
  $s.IconLocation = Join-Path $root "scripts\app-icon.ico"
  $s.WindowStyle = 7  # minimised, so only the browser shows
  $s.Save()
}
Write-Output "Added prep to the Start Menu and Desktop. Right-click it in the Start Menu to pin it to the taskbar."
