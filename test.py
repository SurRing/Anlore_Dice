import re
"""<div id="112952" position="100047" lastactivity="0" duedate="1619798340000" class="sortable_item_row upcoming_item_row row expanded">
        
        <!-- Items Column -->
        <div class="cell gradable">
          第6次测试题（海岸冰川风成地貌，21春 中北）<div class="activityType">
              到期日期: 2021-4-30</div>
          <div class="itemCat">测试</div>
          <div class="eval-links horizontal">
            </div>
        </div>"""
reg = """<div id="(.+)" position="(?:.+)" lastactivity="0" duedate="(.+)" class="sortable_item_row upcoming_item_row row expanded">

    <!-- Items Column -->
    <div class="cell gradable"(?:.*)>
      (.+)<div class="activityType">
          到期日期: (.+)</div>
      <div class="itemCat">(.+)</div>
      <div class="eval-links horizontal">
        </div>
    </div>"""

for line in re.findall(reg, text):
    print(line)