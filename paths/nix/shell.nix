let
    nixpkgs = fetchTarball "https://github.com/NixOs/nixpkgs/tarball/nixos-23.11";
    pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShell {
    packages = with pkgs; [
        git
        neovim
        nodejs
    ];
    GIT_EDITOR = "${pkgs.neovim}/bin/nvim";

    shellHook = ''
        git status
    '';
}