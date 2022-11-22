package cn.repigeons.njnu.classroom.model;

public class Cookies {
    private String name;
    private String value;
    private String domain;
    private String path;

    public static Builder builder() {
        return new Builder();
    }

    public String getName() {
        return name;
    }

    public String getValue() {
        return value;
    }

    public String getDomain() {
        return domain;
    }

    public String getPath() {
        return path;
    }

    public static class Builder {
        private String name;
        private String value;
        private String domain;
        private String path;

        private Builder() {
        }

        public Builder name(String name) {
            this.name = name;
            return this;
        }

        public Builder value(String value) {
            this.value = value;
            return this;
        }

        public Builder domain(String domain) {
            this.domain = domain;
            return this;
        }

        public Builder path(String path) {
            this.path = path;
            return this;
        }

        public Cookies build() {
            Cookies cookies = new Cookies();
            cookies.name = name;
            cookies.value = value;
            cookies.domain = domain;
            cookies.path = path;
            return cookies;
        }
    }
}
