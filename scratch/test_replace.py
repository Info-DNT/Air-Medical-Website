import re

def test():
    samples = [
        '<link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet" media="print" onload="this.media=\'all\'">',
        '<link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet" media="print" onload="this.media=\\\\\'all\\\\\'">',
        '<link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet" media="print" onload="this.media=\\\'all\\\'">',
        '<link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet" media="print" onload="this.media=\'all\'">',
        '<link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet" media="print" onload="this.media=\'all\'">'
    ]
    
    pattern = re.compile(r'onload\s*=\s*"\s*this\.media\s*=\s*\\*\'all\\*\'\s*"', re.IGNORECASE)
    
    for s in samples:
        # We want to replace it with onload="this.media='all'"
        # In python, to write onload="this.media='all'" we can do:
        res = pattern.sub('onload="this.media=\'all\'"', s)
        print(f"Original: {s}")
        print(f"Fixed:    {res}")
        print("-" * 50)

if __name__ == '__main__':
    test()
