
from driver import Driver

# Example URL: https://www.google.com/maps/@19.3027855,-99.1876174,3a,75y,11.99h,90.13t/data=!3m7!1e1!3m5!1syt-CdKZxt9zeBlRmp1Wl-g!2e0!5s20170601T000000!7i13312!8i6656


def main():
    print("-" * 100)
    delete_old = input("Delete old image results? [y/n]: ").lower()
    print("-" * 100)
    url = input("Google Maps URL with historical images: ")
    print("-" * 100)
    name = input("Image tag (no spaces): ")
    print("-" * 100)
    d = Driver()
    if delete_old == "y" or delete_old == "yes":
        d.clean_path()
    d.open_url(url, name)
    d.download_historical_images()
    d.close()


if __name__ == "__main__":
    main()
