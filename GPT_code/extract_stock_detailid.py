from bs4 import BeautifulSoup

html_content = """
<input type="hidden" id="contextPath" value=""/>
<input type="hidden" id="ctrlSuffix" value=".html"/>
<div id="football" class="bbbb">

		<div class="seat-legend">
						<label><span class="cell enable"></span>可预订</label>





						<label><span class="cell disable red"></span>已预订</label><label><span class="cell bad"></span>不可用</label>


					</div>

	<div class="seat-view" style="margin-left: 0;">
		<div class="seat-view-box">
			<ul class="cell-ul cell-vanue-sm" data-col="1"
				data-row="2">
				<li data-row="1"><span class="cell football" title="场地1" data="1" id="seat_1" rel="2"></span></li>
				<li data-row="2"><span class="cell football" title="场地2" data="2" id="seat_2" rel="2"></span></li>

			</ul>
		</div>
	</div>
</div>







	<input type="hidden" value="1_2813413_3,2_2813414_1," id="txt_seatid" />
"""

soup = BeautifulSoup(html_content, 'html.parser')

# 查找 id 为 txt_seatid 的 input 标签
input_tag = soup.find('input', id='txt_seatid')

if input_tag:
    # 获取 value 属性的值
    value = input_tag['value']
    print("提取到的值:", value)
else:
    print("未找到对应的标签")
