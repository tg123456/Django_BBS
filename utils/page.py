class MyPage(object):
    def __init__(self, page_num, all_data_amount, url_prefix, per_page_data=10, page_show_tags=9):

        '''
        :param page_num: 当前页码
        :param all_data_amount:  总的数据量
        :param url_prefix:  页码a标签的url前缀
        :param per_page_data:  每页显示多少条数据
        :param page_show_tags:  页面上显示多少个页码
        '''
        self.page_num = page_num
        self.url_prefix = url_prefix
        self.all_data_amount = all_data_amount
        self.per_page_data = per_page_data
        self.page_show_tags = page_show_tags

        try:
            page_num = int(page_num)
        except Exception:
            page_num = 1
        # 如果当前页码小于等于0，我给你返回第一页
        if page_num <= 0: page_num = 1

        # 通过总数据的条数来计算有多少页,a为商，b为余数，如果余数！=0，总页数=a+1，否则=a
        total_page_num, more = divmod(self.all_data_amount, self.per_page_data)
        if more: total_page_num += 1

        # 如果当前页码大于总的页码数，返回最后一页
        if page_num > total_page_num: page_num = total_page_num

        if total_page_num == 0: page_num = 1

        page_start_num = (page_num - 1) * self.per_page_data
        page_end_num = page_num * self.per_page_data
        self.page_num = page_num
        self.page_start_num = page_start_num
        self.page_end_num = page_end_num
        self.total_page_num = total_page_num

    @property
    def start(self):
        return self.page_start_num

    @property
    def end(self):
        return self.page_end_num

    @property
    def html(self):
        show_tags_left = self.page_num - self.page_show_tags // 2
        show_tags_right = self.page_num + self.page_show_tags // 2

        # 控制两端不超出显示
        if show_tags_left <= 0:
            show_tags_left = 1
            show_tags_right = self.page_show_tags

        if show_tags_right >= self.total_page_num:
            show_tags_right = self.total_page_num
            show_tags_left = self.total_page_num - self.page_show_tags + 1

        if self.total_page_num < self.page_show_tags:
            show_tags_left = 1
            show_tags_right = self.total_page_num

        return self.make_html(show_tags_left, show_tags_right)

    def make_html(self, show_tags_left, show_tags_right):
        start = '<nav aria-label="Page navigation"> <ul class="pagination">'
        end = '</ul></nav>'
        first_page_tag = '<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix)
        last_page_tag = '<li><a href="{}?page={}">尾页</a></li>'.format(self.url_prefix, self.total_page_num)
        front_page_tag = '<li><a href="{}?page={}">&laquo;</a></li>'.format(self.url_prefix, self.page_num - 1)
        next_page_tag = '<li><a href="{}?page={}">&raquo;</a></li>'.format(self.url_prefix, self.page_num + 1)

        page_tag_html = ''
        for i in range(show_tags_left, show_tags_right + 1):
            if i == self.page_num:
                page_tag_html += '<li class="active"><a href="{1}?page={0}">{0}</a></li>'.format(
                    i, self.url_prefix)
            else:
                page_tag_html += '<li><a href="{1}?page={0}">{0}</a></li>'.format(i, self.url_prefix)
        page_tag_html = start + front_page_tag + first_page_tag + page_tag_html + last_page_tag + next_page_tag + end
        return page_tag_html
