import weather_api

MERMAID_FILE = 'weather_diagram.md'
MERMAID_HEADER = "```mermaid\ngraph LR;"


def write_mermaid_md(mermaid_data):
    with open(MERMAID_FILE, 'w') as fp:
        fp.write("%s\n" % MERMAID_HEADER)
        for _ in mermaid_data:
            fp.write("    %s\n" % _)


def generate_mermaid_markdown(zip_code): 
    location_info = weather_api.get_location(zip_code)
    lat = location_info.get('lat')
    lon = location_info.get('lon')
    data = weather_api.get_weather_forecast(lat = lat, lon = lon)

    mermaid_md = []

    for parent, children in data.items():
        get_children(children, parent, mermaid_md)

    write_mermaid_md(mermaid_md)


def get_children(children, parent: str, mermaid_md):
    if isinstance(children, dict):
        for k, v in children.items():
            chain = f"{parent}-->"
            chain += f"{parent}_{k}-->"
            if isinstance(v, dict):
                get_children(v, chain)
            else:
                if isinstance(v, list):
                    counter = 0
                    for _ in v:
                        get_children(_, chain)
                        counter +=1
                else:
                    v = str(v).replace(' ','_')
                    chain += f"{v};"
                    mermaid_md.append(chain)
    else:
        if isinstance(children, list):
            counter = 0
            for _ in children:
                parent =f"{parent}_{counter}"
                get_children(_, parent, mermaid_md)
        else:
            children = str(children).replace(' ','_')
            chain = f"{parent}-->"
            chain += f"{children};"
            mermaid_md.append(chain)


def main():
    generate_mermaid_markdown('32137')


if __name__ == "__main__":
    main()