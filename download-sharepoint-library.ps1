$destination = "C:\\tools\\Folder"
$webUrl = "<Url of the specific site>"
$listUrl = "<Url of the specific list. This url is complete Url and NOT relative url>"
##############################################################

$web = Get-SPWeb -Identity $webUrl
$list = $web.GetList($listUrl)

function ProcessFolder {
    param($folderUrl)
    $folder = $web.GetFolder($folderUrl)
    foreach ($file in $folder.Files) {
        #Ensure destination directory
        $destinationfolder = $destination + "/" + $folder.Url 
        if (!(Test-Path -path $destinationfolder))
        {
            $dest = New-Item $destinationfolder -type directory 
        }
        #Download file
        $binary = $file.OpenBinary()
        $stream = New-Object System.IO.FileStream($destinationfolder + "/" + $file.Name), Create
        $writer = New-Object System.IO.BinaryWriter($stream)
        $writer.write($binary)
        $writer.Close()
        }
}

#Download root files
ProcessFolder($list.RootFolder.Url)
#Download files in folders
foreach ($folder in $list.Folders) {
    ProcessFolder($folder.Url)
}
