# SPDX-License-Identifier: MIT
# Copyright (c) 2026 zhaotingding
# Link one complete local skill into a Windows client skill directory.
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)][string] $Source,
    [Parameter(Mandatory = $true)][string] $Destination
)

$ErrorActionPreference = 'Stop'
if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw 'This helper creates directory junctions on Windows.'
}

$sourceDir = Get-Item -LiteralPath $Source -Force
if (-not $sourceDir.PSIsContainer -or -not (Test-Path -LiteralPath (Join-Path $sourceDir.FullName 'SKILL.md') -PathType Leaf)) {
    throw 'Select a single skill directory containing SKILL.md.'
}
$parentPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination)
$linkPath = Join-Path $parentPath $sourceDir.Name
if ($linkPath -eq $sourceDir.FullName) { "Already installed: $linkPath"; return }
if ($parentPath -eq $sourceDir.FullName -or $parentPath.StartsWith($sourceDir.FullName + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The destination would make the source directory contain its own link.'
}

# Keep existing user skills. Repeating a successful install is a no-op.
$existing = Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue
if ($null -ne $existing) {
    if ($existing.LinkType -in @('Junction','SymbolicLink')) {
        $target = @($existing.Target)[0]
        if ($target) {
            if (-not [IO.Path]::IsPathRooted($target)) { $target = Join-Path $parentPath $target }
            if ([IO.Path]::GetFullPath($target) -eq $sourceDir.FullName) { "Already linked: $linkPath"; return }
        }
    }
    throw "Entry already exists and was preserved: $linkPath"
}
if ($PSCmdlet.ShouldProcess($linkPath, "Create a directory junction to $($sourceDir.FullName)")) {
    [IO.Directory]::CreateDirectory($parentPath) | Out-Null
    New-Item -ItemType Junction -Path $linkPath -Target $sourceDir.FullName | Select-Object FullName, LinkType, Target
}
