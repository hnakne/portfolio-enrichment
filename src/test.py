# import pytest
import main

portfolio_element_example = """
<li class="flex flex-col border-t border-neutral-light cursor-pointer sm:cursor-default pb-20"><div class="flex justify-between items-center"><span class="py-10 text-primary transition-all duration-200"><a class="relative inline-flex items-center text-18 leading-34 font-medium pb-2 transition-hover text-primary group hover:text-secondary focus:text-primary focus:outline-none text-16 !leading-20" href="/current-portfolio/3shape"><span class="inline-block">3Shape</span><svg class="inline-block w-10 h-10 ml-10 fill-current text-primary transition-hover transform rotate-180 group-hover:text-secondary" width="7" height="10" viewBox="0 0 7 10" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M6.41421 8.58579L2.87868 5.05025L6.41421 1.51472L5 0.100506L1.46447 3.63604L0.0502526 5.05025L1.46447 6.46447L5 10L6.41421 8.58579Z"></path></svg><span class="absolute bottom-0 left-0 -right-1 min-w-full h-2 bg-transparent opacity-25 transition-hover group-focus:bg-primary" aria-hidden="true"></span></a></span><span class="inline-flex justify-center items-center transition-hover hover:bg-neutral-lighter-alt group-hover:bg-neutral-lighter-alt focus:ring group-focus:ring focus:ring-primary group-focus:ring-primary focus:outline-none w-30 h-30 rounded-5"><svg class="block fill-current text-primary transform transition-transform duration-100 w-10 h-10 rotate-90" width="7" height="10" viewBox="0 0 7 10" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M6.41421 8.58579L2.87868 5.05025L6.41421 1.51472L5 0.100506L1.46447 3.63604L0.0502526 5.05025L1.46447 6.46447L5 10L6.41421 8.58579Z"></path></svg></span></div><div class="h-0 overflow-hidden transition-all duration-200" style="overflow: hidden; height: 140px;"><div class="flex flex-col"><ul class="tb:pr-15"><li class="flex items-center py-10 text-14 leading-14 text-secondary-darker border-t border-neutral-light"><span class="font-medium w-90 tb:w-120">Sector</span><span class="flex-1 font-light">Healthcare</span></li><li class="flex items-center py-10 text-14 leading-14 text-secondary-darker border-t border-neutral-light"><span class="font-medium w-90 tb:w-120">Country</span><span class="flex-1 font-light">Denmark</span></li><li class="flex items-center py-10 text-14 leading-14 text-secondary-darker border-t border-neutral-light"><span class="font-medium w-90 tb:w-120">Fund</span><span class="flex-1 font-light"><ul><li><a class="text-primary font-medium" href="/current-portfolio/funds/eqt-ix">EQT IX</a></li></ul></span></li><li class="flex items-center py-10 text-14 leading-14 text-secondary-darker border-t border-neutral-light"><span class="font-medium w-90 tb:w-120">Entry</span><span class="flex-1 font-light">2022</span></li></ul></div></div></li>
"""


def test_element_parsing_happy_path():
    with open('list_item_example.html') as f:
        example_list_item = f.read()
        list_item = main.soup_from_string(example_list_item)
        parsed_item = main.parse_portfolio_list_element(list_item)
        assert parsed_item['name'] == 'Guardian Shanghai Hygiene Service Ltd'
        assert 'parse_error' not in parsed_item
        assert 'raw_html' in parsed_item

# Todo add tests