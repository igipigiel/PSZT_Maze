function [] = remake_latex(filename)
x = [];
fid = fopen(filename, 'r');
fid_e = fopen(strcat(filename(1:end-4),'_edited.txt'), 'w')
a = 10;
while feof(fid) == 0
        temp = fgetl(fid);
        temp_form = sscanf(temp, '%f')

        fprintf(fid_e,'%d %f', a, temp_form(1));
        fprintf(fid_e,'%s', newline)

        a = a + 1;
end
fclose(fid);
fclose(fid_e);
end

